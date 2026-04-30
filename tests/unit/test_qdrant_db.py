from __future__ import annotations


def test_create_collection_uses_cosine_vector_configuration(fresh_import):
    qdrant_db = fresh_import("src.database.qdrant_db")

    qdrant_db.create_collection(vector_size=3)

    request = qdrant_db.client.recreated_collections[-1]
    assert request["collection_name"] == "legal_docs"
    assert request["vectors_config"].size == 3
    assert request["vectors_config"].distance == "cosine"


def test_insert_batch_converts_embeddings_to_qdrant_points(fresh_import):
    qdrant_db = fresh_import("src.database.qdrant_db")

    qdrant_db.insert_batch(
        start_id=10,
        embeddings=[_Embedding([1.0, 2.0]), _Embedding([3.0, 4.0])],
        texts=["Section 1", "Section 2"],
    )

    upsert = qdrant_db.client.upserts[-1]
    assert upsert["collection_name"] == "legal_docs"
    assert upsert["wait"] is True
    assert [(point.id, point.vector, point.payload) for point in upsert["points"]] == [
        (10, [1.0, 2.0], {"text": "Section 1"}),
        (11, [3.0, 4.0], {"text": "Section 2"}),
    ]


def test_search_converts_query_embedding_to_vector(fresh_import):
    qdrant_db = fresh_import("src.database.qdrant_db")
    qdrant_db.client.search_results = ["result"]

    results = qdrant_db.search(_Embedding([0.1, 0.2]))

    assert results == ["result"]
    assert qdrant_db.client.searches[-1] == {
        "collection_name": "legal_docs",
        "query_vector": [0.1, 0.2],
        "limit": 5,
    }


class _Embedding:
    def __init__(self, values):
        self.values = values

    def tolist(self):
        return list(self.values)
