from __future__ import annotations


def test_reranking_pipeline_returns_documents_in_descending_score_order(fresh_import):
    reranker = fresh_import("src.rag.reranker")
    documents = [
        "minor result",
        "substantially more relevant result by score",
        "middle result",
    ]

    assert reranker.rerank("legal remedy", documents) == [
        "substantially more relevant result by score",
        "middle result",
        "minor result",
    ]
