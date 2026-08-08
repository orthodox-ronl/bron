#!/usr/bin/env python3
"""Inject TermRefs for MRG formPhrases into generated glossary.md (pre-TRRT).

Runs after HRGT + sort, before TRRT. Wraps plain occurrences of defined
formPhrases as ``[match](term@)`` or ``[match](term@scopetag)`` when the entry
scopetag differs from the glossary default scope.

Self-term formPhrases are not wrapped (definition or notes). Existing markdown
links, TermRefs, and inline code are left untouched.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

TABLE_SEPARATOR_RE = re.compile(
    r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$"
)
TERM_FROM_LINK_RE = re.compile(
    r"\]\((?:https?://[^)]+/)?(?:(?:\.\./)*terms/|(?:\.\./)*terminologie/)?"
    r"([a-z0-9][a-z0-9_-]*)(?:\.md)?/?\)",
    re.IGNORECASE,
)
TERMREF_OR_LINK_RE = re.compile(r"\[[^\]]*\]\([^)]*\)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
HTML_TAG_RE = re.compile(r"<[^>]+>")
MORPH_RE = re.compile(r"[{}]")
# TRRT showtext may not contain '@' (see TEv2 TermRef regex). Alias/abbr rows
# for terms like @include-vsa otherwise leave [@include-vsa](include-vsa@).
TERMREF_AT_IN_SHOWTEXT_RE = re.compile(
    r"\[([^\]\n]*@[^\]\n]*)\]\(([^)\n]*@[a-z0-9_:-]*)\)",
    re.IGNORECASE,
)


def split_markdown_table_row(row: str) -> list[str]:
    text = row.strip()
    if text.startswith("|"):
        text = text[1:]
    if text.endswith("|"):
        text = text[:-1]

    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for char in text:
        if escaped:
            current.append(char)
            escaped = False
        elif char == "\\":
            current.append(char)
            escaped = True
        elif char == "|":
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    cells.append("".join(current).strip())
    return cells


def join_markdown_table_row(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def load_mrg_entries(mrgs_dir: Path) -> list[dict]:
    entries: list[dict] = []
    if not mrgs_dir.is_dir():
        return entries
    for path in sorted(mrgs_dir.glob("mrg.*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for entry in data.get("entries") or []:
            if isinstance(entry, dict) and entry.get("term"):
                entries.append(entry)
    return entries


def default_scopetag(mrgs_dir: Path, saf_path: Path | None) -> str:
    if saf_path and saf_path.is_file():
        saf = yaml.safe_load(saf_path.read_text(encoding="utf-8")) or {}
        # SAF shapes: {scope: {scopetag: …}} or top-level scopetag
        scope = (saf.get("scope") or {}).get("scopetag") or saf.get("scopetag")
        if scope:
            return str(scope)
    for path in sorted(mrgs_dir.glob("mrg.*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        term = data.get("terminology") or {}
        if term.get("scopetag"):
            return str(term["scopetag"])
    return ""


def build_phrase_index(
    entries: list[dict], default_scope: str
) -> list[tuple[str, str, str]]:
    """Return (phrase, term, ref_suffix) sorted longest-phrase first."""
    by_phrase: dict[str, tuple[str, str, str]] = {}
    for entry in entries:
        term = str(entry["term"])
        scope = str(entry.get("scopetag") or default_scope or "")
        ref_suffix = "" if (not scope or scope == default_scope) else scope
        phrases = list(entry.get("formPhrases") or [])
        for extra in (
            entry.get("glossaryTerm"),
            entry.get("glossaryAbbr"),
            entry.get("glossaryAlias"),
            term,
        ):
            if extra:
                phrases.append(str(extra))
        for raw in phrases:
            phrase = str(raw).strip()
            if not phrase or MORPH_RE.search(phrase):
                continue
            key = phrase.casefold()
            if key not in by_phrase:
                by_phrase[key] = (phrase, term, ref_suffix)
                continue
            old_phrase, old_term, _old_suf = by_phrase[key]
            if len(phrase) > len(old_phrase):
                by_phrase[key] = (phrase, term, ref_suffix)
            elif (
                len(phrase) == len(old_phrase)
                and old_term.casefold() != key
                and term.casefold() == key
            ):
                by_phrase[key] = (phrase, term, ref_suffix)
    indexed = list(by_phrase.values())
    indexed.sort(key=lambda item: len(item[0]), reverse=True)
    return indexed


def own_term_keys(entry_term: str, entries: list[dict]) -> set[str]:
    keys = {entry_term.casefold()}
    for entry in entries:
        if str(entry.get("term")) != entry_term:
            continue
        for raw in entry.get("formPhrases") or []:
            keys.add(str(raw).strip().casefold())
        for extra in (
            entry.get("glossaryTerm"),
            entry.get("glossaryAbbr"),
            entry.get("glossaryAlias"),
        ):
            if extra:
                keys.add(str(extra).strip().casefold())
    return {k for k in keys if k}


def protected_spans(text: str) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    for pattern in (TERMREF_OR_LINK_RE, INLINE_CODE_RE, HTML_TAG_RE):
        for match in pattern.finditer(text):
            spans.append((match.start(), match.end()))
    spans.sort()
    return spans


def is_protected(spans: list[tuple[int, int]], start: int, end: int) -> bool:
    for a, b in spans:
        if start < b and end > a:
            return True
    return False


def sanitize_termref_showtexts(text: str) -> str:
    """Strip '@' from TermRef showtext so TRRT can resolve the reference."""

    def repl(match: re.Match[str]) -> str:
        show = match.group(1).replace("@", "")
        if not show:
            show = match.group(2).split("@", 1)[0] or match.group(1)
        return f"[{show}]({match.group(2)})"

    return TERMREF_AT_IN_SHOWTEXT_RE.sub(repl, text)


def inject_into_text(
    text: str,
    phrases: list[tuple[str, str, str]],
    skip_terms: set[str],
) -> str:
    if not text:
        return text
    text = sanitize_termref_showtexts(text)
    occupied: list[tuple[int, int]] = protected_spans(text)
    replacements: list[tuple[int, int, str]] = []

    for phrase, term, ref_suffix in phrases:
        if term.casefold() in skip_terms or phrase.casefold() in skip_terms:
            continue
        pattern = re.compile(
            rf"(?<![A-Za-z0-9_-])({re.escape(phrase)})(?![A-Za-z0-9_-])",
            re.IGNORECASE,
        )
        for match in pattern.finditer(text):
            start, end = match.start(1), match.end(1)
            if is_protected(occupied, start, end):
                continue
            show = match.group(1)
            if ref_suffix:
                repl = f"[{show}]({term}@{ref_suffix})"
            else:
                repl = f"[{show}]({term}@)"
            replacements.append((start, end, repl))
            occupied.append((start, end))

    if not replacements:
        return text
    replacements.sort(key=lambda item: item[0])
    parts: list[str] = []
    cursor = 0
    for start, end, repl in replacements:
        if start < cursor:
            continue
        parts.append(text[cursor:start])
        parts.append(repl)
        cursor = end
    parts.append(text[cursor:])
    return "".join(parts)


def term_id_from_first_cell(cell: str) -> str | None:
    match = TERM_FROM_LINK_RE.search(cell)
    if match:
        return match.group(1)
    return None


def process_glossary(
    text: str,
    phrases: list[tuple[str, str, str]],
    entries: list[dict],
) -> str:
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        if (
            i + 1 < len(lines)
            and lines[i].lstrip().startswith("|")
            and TABLE_SEPARATOR_RE.match(lines[i + 1])
        ):
            out.append(lines[i])
            out.append(lines[i + 1])
            i += 2
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                row = lines[i]
                cells = split_markdown_table_row(row)
                if len(cells) >= 2:
                    term_id = term_id_from_first_cell(cells[0])
                    skip = own_term_keys(term_id, entries) if term_id else set()
                    cells[1] = inject_into_text(cells[1], phrases, skip)
                    row = join_markdown_table_row(cells)
                out.append(row)
                i += 1
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inject TermRefs for formPhrases into generated glossary.md"
    )
    parser.add_argument(
        "glossary",
        nargs="?",
        default="glossary.md",
        type=Path,
        help="Path to generated glossary.md (cwd usually generated/docs)",
    )
    parser.add_argument(
        "--mrgs-dir",
        type=Path,
        default=None,
        help="Directory with mrg.*.yaml (default: <glossary-dir>/mrgs)",
    )
    parser.add_argument(
        "--saf",
        type=Path,
        default=None,
        help="Optional saf.yaml for default scopetag",
    )
    args = parser.parse_args()
    glossary_path: Path = args.glossary
    mrgs_dir = args.mrgs_dir or (glossary_path.parent / "mrgs")
    saf_path = args.saf or (glossary_path.parent / "saf.yaml")

    entries = load_mrg_entries(mrgs_dir)
    if not entries:
        print(f"WARNING: no MRG entries in {mrgs_dir}; skipping TermRef inject")
        return 0

    default_scope = default_scopetag(
        mrgs_dir, saf_path if saf_path.is_file() else None
    )
    phrases = build_phrase_index(entries, default_scope)
    original = glossary_path.read_text(encoding="utf-8")
    updated = process_glossary(original, phrases, entries)
    glossary_path.write_text(updated, encoding="utf-8")
    print(
        f"Injected glossary TermRefs: {glossary_path} "
        f"({len(phrases)} phrases, default scope={default_scope!r})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
