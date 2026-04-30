from __future__ import annotations


def test_empty_query_flows_to_retrieval_layer(monkeypatch, fresh_import):
    chatbot = fresh_import("src.chatbot.chatbot")
    calls = []

    monkeypatch.setattr(chatbot, "retrieve", lambda question: calls.append(question) or "No relevant legal document found.")

    assert chatbot.ask_chatbot("") == "No relevant legal document found."
    assert calls == [""]


def test_large_input_text_is_passed_without_truncation(monkeypatch, fresh_import):
    chatbot = fresh_import("src.chatbot.chatbot")
    large_query = "legal remedy " * 1000
    captured = {}

    def fake_retrieve(question):
        captured["question"] = question
        return "large input handled"

    monkeypatch.setattr(chatbot, "retrieve", fake_retrieve)

    assert chatbot.ask_chatbot(large_query) == "large input handled"
    assert captured["question"] == large_query


def test_no_retrieval_results_return_stable_user_message(monkeypatch, fresh_import):
    retriever = fresh_import("src.rag.retriever")

    monkeypatch.setattr(retriever, "get_embedding", lambda query: _Embedding([0.0]))
    monkeypatch.setattr(retriever, "search", lambda embedding: [])

    assert retriever.retrieve("not in corpus") == "No relevant legal document found."


class _Embedding:
    def __init__(self, values):
        self.values = values

    def tolist(self):
        return list(self.values)
