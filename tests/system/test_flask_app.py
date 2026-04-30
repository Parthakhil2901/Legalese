from __future__ import annotations

import pytest


def test_flask_application_factory_or_app_object_is_available(fresh_import):
    app_module = fresh_import("app")
    flask_app = getattr(app_module, "app", None)
    create_app = getattr(app_module, "create_app", None)

    if flask_app is None and create_app is None:
        pytest.skip("No Flask app or create_app factory exists in the current application.")

    app = flask_app if flask_app is not None else create_app()
    assert hasattr(app, "test_client")
