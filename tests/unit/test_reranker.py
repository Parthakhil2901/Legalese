from __future__ import annotations


def test_rerank_orders_documents_by_model_score(fresh_import):
    reranker = fresh_import("src.rag.reranker")

    ranked = reranker.rerank("bail", ["short", "the longest legal passage", "medium text"])

    assert ranked == ["the longest legal passage", "medium text", "short"]


def test_rerank_returns_empty_list_for_empty_documents(fresh_import):
    reranker = fresh_import("src.rag.reranker")

    assert reranker.rerank("query", []) == []
