from pathlib import Path
from typing import Any

from .ocr import read_text, read_words
from .patterns import parse_lines
from .preprocess import prepare_image


def extract(image: str | Path, *, lang: str = "por", preprocess: bool = True, include_words: bool = False) -> dict[str, Any]:
    prepared = prepare_image(image) if preprocess else prepare_image(image, scale=1)
    text = read_text(prepared, lang=lang)
    result: dict[str, Any] = {
        "text": text,
        "fields": parse_lines(text),
        "metadata": {"engine": "tesseract", "language": lang},
    }
    if include_words:
        result["words"] = read_words(prepared, lang=lang)
    return result
