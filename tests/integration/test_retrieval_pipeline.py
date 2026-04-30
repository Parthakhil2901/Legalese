from __future__ import annotations


def test_retrieval_pipeline_embedding_to_vector_search(monkeypatch, fresh_import, payload_result):
    retriever = fresh_import("src.rag.retriever")
    seen = {}

    def fake_embedding(query):
        seen["query"] = query
        return _Embedding([0.5, 0.25])

    def fake_search(embedding):
        seen["embedding"] = embedding.tolist()
        return [payload_result("IPC 378 defines theft.")]

    monkeypatch.setattr(retriever, "get_embedding", fake_embedding)
    monkeypatch.setattr(retriever, "search", fake_search)

    assert retriever.retrieve("What is theft?") == "IPC 378 defines theft."
    assert seen == {"query": "What is theft?", "embedding": [0.5, 0.25]}


class _Embedding:
    def __init__(self, values):
        self.values = values

    def tolist(self):
        return list(self.values)
