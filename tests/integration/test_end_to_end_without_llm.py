from __future__ import annotations


def test_end_to_end_query_flow_without_llm_call(monkeypatch, fresh_import, payload_result):
    retriever = fresh_import("src.rag.retriever")
    chatbot = fresh_import("src.chatbot.chatbot")

    monkeypatch.setattr(retriever, "get_embedding", lambda query: _Embedding([1.0, 0.0]))
    monkeypatch.setattr(retriever, "search", lambda embedding: [payload_result("IPC 420 covers cheating.")])
    monkeypatch.setattr(chatbot, "retrieve", retriever.retrieve)

    assert chatbot.ask_chatbot("cheating legal section") == "IPC 420 covers cheating."


class _Embedding:
    def __init__(self, values):
        self.values = values

    def tolist(self):
        return list(self.values)
