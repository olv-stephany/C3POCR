from typing import Any

import pytesseract
from PIL import Image
from pytesseract import Output


def read_text(image: Image.Image, lang: str = "por", config: str = "--psm 6") -> str:
    return pytesseract.image_to_string(image, lang=lang, config=config).strip()


def read_words(image: Image.Image, lang: str = "por", config: str = "--psm 6") -> list[dict[str, Any]]:
    data = pytesseract.image_to_data(image, lang=lang, config=config, output_type=Output.DICT)
    words = []
    for index, text in enumerate(data["text"]):
        text = text.strip()
        if not text:
            continue
        try:
            confidence = float(data["conf"][index])
        except (TypeError, ValueError):
            confidence = -1.0
        words.append({
            "text": text,
            "confidence": confidence,
            "left": data["left"][index],
            "top": data["top"][index],
            "width": data["width"][index],
            "height": data["height"][index],
            "line_num": data["line_num"][index],
        })
    return words
