from pathlib import Path
from typing import Any

from .ocr import read_words
from .patterns import parse_lines
from .preprocess import prepare_image
from .layout import detect_titles, group_blocks, group_lines, group_sections
from .regions import build_regions


def extract(
    image: str | Path,
    *,
    lang: str = "por",
    config: str = "--psm 11",
    preprocess: bool = True,
    include_words: bool = False,
) -> dict[str, Any]:
    prepared = prepare_image(image) if preprocess else prepare_image(image, scale=1)
    words = read_words(prepared, lang=lang, config=config)
    lines = group_lines(words)
    text = "\n".join(line["text"] for line in lines)
    detailed_groups = group_sections(lines, include_lines=True)
    groups = [{key: value for key, value in group.items() if key != "lines"} for group in detailed_groups]
    regions = build_regions(detailed_groups)
    result: dict[str, Any] = {
        "text": text,
        "fields": parse_lines(text),
        "metadata": {"engine": "tesseract", "language": lang, "config": config},
        "groups": groups,
        "regions": regions,
        "layout": {},
    }
    if include_words:
        result["layout"].update({
            "lines": lines,
            "blocks": group_blocks(lines),
            "titles": detect_titles(lines),
            "groups": detailed_groups,
        })
        result["words"] = words
    if not result["layout"]:
        del result["layout"]
    return result
