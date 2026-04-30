from __future__ import annotations

import pytest


def test_query_endpoint_schema_and_status(monkeypatch, fresh_import):
    flask_app = _get_flask_app_or_skip(fresh_import)

    import src.chatbot.chatbot as chatbot

    monkeypatch.setattr(chatbot, "ask_chatbot", lambda question: "mock legal response")
    client = flask_app.test_client()

    response = client.post("/query", json={"query": "What is theft?"})

    assert response.status_code == 200
    payload = response.get_json()
    assert isinstance(payload, dict)
    assert "response" in payload or "answer" in payload


def test_query_endpoint_rejects_invalid_input(fresh_import):
    flask_app = _get_flask_app_or_skip(fresh_import)
    client = flask_app.test_client()

    response = client.post("/query", json={})

    assert response.status_code in {400, 422}


def _get_flask_app_or_skip(fresh_import):
    app_module = fresh_import("app")
    flask_app = getattr(app_module, "app", None)
    create_app = getattr(app_module, "create_app", None)
    if flask_app is None and create_app is None:
        pytest.skip("No Flask query endpoint exists in the current application.")
    return flask_app if flask_app is not None else create_app()
