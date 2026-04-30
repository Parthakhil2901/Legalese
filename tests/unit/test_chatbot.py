from __future__ import annotations


def test_ask_chatbot_delegates_question_to_retriever(monkeypatch, fresh_import):
    chatbot = fresh_import("src.chatbot.chatbot")
    calls = []

    def fake_retrieve(question):
        calls.append(question)
        return "retrieved answer"

    monkeypatch.setattr(chatbot, "retrieve", fake_retrieve)

    assert chatbot.ask_chatbot("What is theft?") == "retrieved answer"
    assert calls == ["What is theft?"]
