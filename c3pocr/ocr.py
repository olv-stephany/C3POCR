import shutil
from functools import lru_cache
from pathlib import Path
from typing import Any

import pytesseract
from PIL import Image
from pytesseract import Output


@lru_cache(maxsize=8)
def configure_tesseract(tesseract_cmd: str | Path | None = None) -> str:
    """Configura o executável local ou usa o Tesseract disponível no PATH."""
    if tesseract_cmd is None:
        project_root = Path(__file__).resolve().parents[1]
        bundled_paths = (
            project_root / "tools" / "tesseract.exe",
            project_root / "tools" / "tesseract" / "tesseract.exe",
        )
        tesseract_cmd = next((path for path in bundled_paths if path.exists()), None)
        tesseract_cmd = tesseract_cmd or shutil.which("tesseract")

    if not tesseract_cmd:
        raise FileNotFoundError(
            "Tesseract não encontrado. Coloque-o em tools\\tesseract.exe "
            "ou instale-o no PATH."
        )

    command = str(tesseract_cmd)
    pytesseract.pytesseract.tesseract_cmd = command
    return command


def read_text(image: Image.Image, lang: str = "por", config: str = "--psm 11") -> str:
    configure_tesseract()
    return pytesseract.image_to_string(image, lang=lang, config=config).strip()


def read_words(image: Image.Image, lang: str = "por", config: str = "--psm 11") -> list[dict[str, Any]]:
    configure_tesseract()
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
        if confidence < 40:
            continue
        words.append({
            "text": text,
            "confidence": confidence,
            "left": data["left"][index],
            "top": data["top"][index],
            "width": data["width"][index],
            "height": data["height"][index],
                "block_num": data["block_num"][index],
                "par_num": data["par_num"][index],
            "line_num": data["line_num"][index],
        })
    return words
