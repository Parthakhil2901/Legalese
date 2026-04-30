from __future__ import annotations

from io import BytesIO

import pytest


def test_query_endpoint_rejects_empty_query(fresh_import):
    flask_app = _get_flask_app_or_skip(fresh_import)
    response = flask_app.test_client().post("/query", json={"query": ""})

    assert response.status_code in {400, 422}


def test_document_upload_endpoint_rejects_corrupted_document(fresh_import):
    flask_app = _get_flask_app_or_skip(fresh_import)
    response = flask_app.test_client().post(
        "/upload",
        data={"file": (BytesIO(b"\x00\xff\x00\xff"), "corrupted.pdf")},
        content_type="multipart/form-data",
    )

    assert response.status_code in {400, 415, 422}


def _get_flask_app_or_skip(fresh_import):
    app_module = fresh_import("app")
    flask_app = getattr(app_module, "app", None)
    create_app = getattr(app_module, "create_app", None)
    if flask_app is None and create_app is None:
        pytest.skip("No Flask API exists in the current application.")
    return flask_app if flask_app is not None else create_app()
