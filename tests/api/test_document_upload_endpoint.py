from __future__ import annotations

from io import BytesIO

import pytest


def test_document_upload_endpoint_accepts_file(fresh_import):
    flask_app = _get_flask_app_or_skip(fresh_import)
    client = flask_app.test_client()

    response = client.post(
        "/upload",
        data={"file": (BytesIO(b"Section 1\nLegal document text"), "sample.txt")},
        content_type="multipart/form-data",
    )

    assert response.status_code in {200, 201, 202}
    assert isinstance(response.get_json(silent=True), dict)


def test_document_upload_endpoint_rejects_missing_file(fresh_import):
    flask_app = _get_flask_app_or_skip(fresh_import)
    client = flask_app.test_client()

    response = client.post("/upload", data={}, content_type="multipart/form-data")

    assert response.status_code in {400, 422}


def _get_flask_app_or_skip(fresh_import):
    app_module = fresh_import("app")
    flask_app = getattr(app_module, "app", None)
    create_app = getattr(app_module, "create_app", None)
    if flask_app is None and create_app is None:
        pytest.skip("No Flask document upload endpoint exists in the current application.")
    return flask_app if flask_app is not None else create_app()
