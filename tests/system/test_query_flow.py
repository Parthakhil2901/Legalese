from __future__ import annotations


def test_full_query_flow_returns_generated_response_with_mocked_retrieval_and_generation(monkeypatch, fresh_import):
    chatbot = fresh_import("src.chatbot.chatbot")

    def fake_retrieve(question):
        assert question == "What is criminal intimidation?"
        return "IPC 503 defines criminal intimidation."

    def fake_generate(context, question):
        return f"Answer: {context} Question: {question}"

    monkeypatch.setattr(chatbot, "retrieve", lambda question: fake_generate(fake_retrieve(question), question))

    assert chatbot.ask_chatbot("What is criminal intimidation?") == (
        "Answer: IPC 503 defines criminal intimidation. Question: What is criminal intimidation?"
    )
