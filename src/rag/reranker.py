from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-reranker-large")
model = AutoModelForSequenceClassification.from_pretrained("BAAI/bge-reranker-large")

model.eval()

def rerank(query, documents):

    scores = []

    for doc in documents:

        inputs = tokenizer(query, doc, return_tensors="pt", truncation=True)

        with torch.no_grad():
            outputs = model(**inputs)

        score = outputs.logits.item()

        scores.append(score)

    ranked_docs = [doc for _, doc in sorted(zip(scores, documents), reverse=True)]

    return ranked_docs