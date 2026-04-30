from __future__ import annotations


def test_get_embedding_uses_configured_model_with_normalization(fresh_import):
    embedder = fresh_import("src.embeddings.embedder")

    embedding = embedder.get_embedding("legal query")

    assert embedding.tolist() == [11.0, 1.0, 42.0]
    assert embedder.model.model_name == "BAAI/bge-large-en-v1.5"
    assert embedder.model.calls == [{"text": "legal query", "normalize_embeddings": True}]


def test_get_embedding_is_deterministic_with_stubbed_model(fresh_import):
    embedder = fresh_import("src.embeddings.embedder")

    first = embedder.get_embedding("same text").tolist()
    second = embedder.get_embedding("same text").tolist()

    assert first == second
