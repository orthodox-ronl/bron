from pathlib import Path


WORKFLOW = Path(".github/workflows/docs-pages.yml")


def test_docs_pages_workflow_exists():
    assert WORKFLOW.exists()


def test_docs_pages_splits_build_and_deploy():
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "build:" in text
    assert "deploy:" in text
    assert "needs: build" in text


def test_docs_pages_uses_reusable_deploy_workflow():
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "pages-deploy-reusable.yml" in text
    assert "orthodox-ronl/VSA-tooling" in text
    assert "artifact_name: pages-docs-site" in text


def test_docs_pages_does_not_use_deploy_pages():
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "actions/deploy-pages" not in text
    assert "actions/upload-pages-artifact" not in text


def test_docs_pages_sets_preview_and_production_outputs():
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "url_prefix=/bron/" in text
    assert "url_prefix=/bron/preview/" in text
    assert "destination_dir=preview" in text
