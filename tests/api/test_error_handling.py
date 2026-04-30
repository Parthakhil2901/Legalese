from __future__ import annotations

import pytest


def test_unknown_api_route_returns_not_found(fresh_import):
    app_module = fresh_import("app")
    flask_app = getattr(app_module, "app", None)
    create_app = getattr(app_module, "create_app", None)
    if flask_app is None and create_app is None:
        pytest.skip("No Flask app exists in the current application.")

    app = flask_app if flask_app is not None else create_app()
    response = app.test_client().get("/does-not-exist")

    assert response.status_code == 404
