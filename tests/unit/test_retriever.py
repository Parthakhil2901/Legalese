from __future__ import annotations


def test_retrieve_returns_best_match_text(monkeypatch, fresh_import, payload_result):
    retriever = fresh_import("src.rag.retriever")
    monkeypatch.setattr(retriever, "get_embedding", lambda query: _Embedding([1.0, 2.0]))
    monkeypatch.setattr(
        retriever,
        "search",
        lambda embedding: [payload_result("Best IPC section"), payload_result("Second match")],
    )

    assert retriever.retrieve("theft punishment") == "Best IPC section"


def test_retrieve_returns_message_when_no_results(monkeypatch, fresh_import):
    retriever = fresh_import("src.rag.retriever")
    monkeypatch.setattr(retriever, "get_embedding", lambda query: _Embedding([1.0]))
    monkeypatch.setattr(retriever, "search", lambda embedding: [])

    assert retriever.retrieve("unknown") == "No relevant legal document found."


class _Embedding:
    def __init__(self, values):
        self.values = values

    def tolist(self):
        return list(self.values)
