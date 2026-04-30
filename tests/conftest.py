from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


class FakeEmbedding:
    def __init__(self, values):
        self.values = list(values)

    def __len__(self):
        return len(self.values)

    def __eq__(self, other):
        return list(other) == self.values if not isinstance(other, FakeEmbedding) else other.values == self.values

    def tolist(self):
        return list(self.values)


class FakeSentenceTransformer:
    def __init__(self, model_name):
        self.model_name = model_name
        self.calls = []

    def encode(self, text, normalize_embeddings=False):
        self.calls.append({"text": text, "normalize_embeddings": normalize_embeddings})
        return FakeEmbedding([float(len(text)), 1.0 if normalize_embeddings else 0.0, 42.0])


class FakeQdrantClient:
    def __init__(self, *args, **kwargs):
        self.init_args = args
        self.init_kwargs = kwargs
        self.recreated_collections = []
        self.upserts = []
        self.searches = []
        self.search_results = []

    def recreate_collection(self, **kwargs):
        self.recreated_collections.append(kwargs)

    def upsert(self, **kwargs):
        self.upserts.append(kwargs)

    def search(self, **kwargs):
        self.searches.append(kwargs)
        return list(self.search_results)


class FakeVectorParams:
    def __init__(self, size, distance):
        self.size = size
        self.distance = distance


class FakePointStruct:
    def __init__(self, id, vector, payload):
        self.id = id
        self.vector = vector
        self.payload = payload


class FakeTokenizer:
    @classmethod
    def from_pretrained(cls, model_name):
        tokenizer = cls()
        tokenizer.model_name = model_name
        return tokenizer

    def __call__(self, query, doc, return_tensors=None, truncation=None):
        return {"query": query, "doc": doc, "return_tensors": return_tensors, "truncation": truncation}


class FakeLogits:
    def __init__(self, value):
        self.value = value

    def item(self):
        return self.value


class FakeModelOutput:
    def __init__(self, score):
        self.logits = FakeLogits(score)


class FakeSequenceClassificationModel:
    @classmethod
    def from_pretrained(cls, model_name):
        model = cls()
        model.model_name = model_name
        return model

    def eval(self):
        self.evaluated = True

    def __call__(self, **inputs):
        return FakeModelOutput(float(len(inputs["doc"])))


class FakeNoGrad:
    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc, tb):
        return False


@pytest.fixture(autouse=True)
def stub_external_dependencies(monkeypatch):
    sentence_transformers = types.ModuleType("sentence_transformers")
    sentence_transformers.SentenceTransformer = FakeSentenceTransformer
    monkeypatch.setitem(sys.modules, "sentence_transformers", sentence_transformers)

    qdrant_client = types.ModuleType("qdrant_client")
    qdrant_client.QdrantClient = FakeQdrantClient
    qdrant_models = types.ModuleType("qdrant_client.models")
    qdrant_models.VectorParams = FakeVectorParams
    qdrant_models.Distance = types.SimpleNamespace(COSINE="cosine")
    qdrant_models.PointStruct = FakePointStruct
    monkeypatch.setitem(sys.modules, "qdrant_client", qdrant_client)
    monkeypatch.setitem(sys.modules, "qdrant_client.models", qdrant_models)

    transformers = types.ModuleType("transformers")
    transformers.AutoTokenizer = FakeTokenizer
    transformers.AutoModelForSequenceClassification = FakeSequenceClassificationModel
    monkeypatch.setitem(sys.modules, "transformers", transformers)

    torch = types.ModuleType("torch")
    torch.no_grad = FakeNoGrad
    monkeypatch.setitem(sys.modules, "torch", torch)


@pytest.fixture
def fresh_import():
    def _fresh_import(module_name):
        sys.modules.pop(module_name, None)
        return importlib.import_module(module_name)

    return _fresh_import


@pytest.fixture
def payload_result():
    def _payload_result(text):
        return types.SimpleNamespace(payload={"text": text})

    return _payload_result
