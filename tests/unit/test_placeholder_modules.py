from __future__ import annotations

import inspect

import pytest


@pytest.mark.parametrize(
    "module_name",
    [
        "src.data_processing.preprocess",
        "src.document_processing.chunker",
        "src.document_processing.text_cleaner",
        "src.document_processing.pdf_loader",
        "src.data_processing.language_detector",
        "src.multilingual.translator",
    ],
)
def test_placeholder_modules_import_without_side_effects(module_name, fresh_import):
    module = fresh_import(module_name)

    assert inspect.ismodule(module)
