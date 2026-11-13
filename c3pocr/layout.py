from statistics import median
from typing import Any


def _box(words: list[dict[str, Any]]) -> dict[str, int]:
    left = min(word["left"] for word in words)
    top = min(word["top"] for word in words)
    right = max(word["left"] + word["width"] for word in words)
    bottom = max(word["top"] + word["height"] for word in words)
    return {"left": left, "top": top, "width": right - left, "height": bottom - top}


def _lines_box(lines: list[dict[str, Any]]) -> dict[str, int]:
    left = min(line["box"]["left"] for line in lines)
    top = min(line["box"]["top"] for line in lines)
    right = max(line["box"]["left"] + line["box"]["width"] for line in lines)
    bottom = max(line["box"]["top"] + line["box"]["height"] for line in lines)
    return {"left": left, "top": top, "width": right - left, "height": bottom - top}


def group_lines(words: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Agrupa palavras da mesma linha usando os identificadores do Tesseract."""
    groups: dict[tuple[int, int, int], list[dict[str, Any]]] = {}
    for word in words:
        key = (word.get("block_num", 0), word.get("par_num", 0), word.get("line_num", 0))
        groups.setdefault(key, []).append(word)

    lines = []
    for key, line_words in groups.items():
        ordered = sorted(line_words, key=lambda word: word["left"])
        heights = [word["height"] for word in ordered if word["height"] > 0]
        # Vãos pequenos podem ser rótulo + valor; vãos muito grandes tendem a ser colunas.
        gap_limit = max(180, median(heights) * 2.5) if heights else 180
        segments: list[list[dict[str, Any]]] = [[ordered[0]]]
        for word in ordered[1:]:
            previous = segments[-1][-1]
            gap = word["left"] - (previous["left"] + previous["width"])
            if gap > gap_limit:
                segments.append([])
            segments[-1].append(word)

        for segment in segments:
            confidence = [word["confidence"] for word in segment if word["confidence"] >= 0]
            lines.append({
                "text": " ".join(word["text"] for word in segment),
                "box": _box(segment),
                "confidence": round(sum(confidence) / len(confidence), 2) if confidence else -1,
                "word_count": len(segment),
                "block_num": key[0],
                "par_num": key[1],
                "line_num": key[2],
            })
    return sorted(lines, key=lambda line: (line["box"]["top"], line["box"]["left"]))


def group_blocks(lines: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Agrupa linhas por bloco visual identificado pelo Tesseract."""
    groups: dict[int, list[dict[str, Any]]] = {}
    for line in lines:
        groups.setdefault(line["block_num"], []).append(line)

    blocks = []
    for block_num, block_lines in groups.items():
        blocks.append(
            {
                "block_num": block_num,
                "text": "\n".join(line["text"] for line in block_lines),
                "lines": block_lines,
                "box": _lines_box(block_lines),
            }
        )
    return sorted(blocks, key=lambda block: (block["box"]["top"], block["box"]["left"]))


def detect_titles(lines: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Marca linhas curtas e visualmente maiores como possíveis títulos."""
    heights = [line["box"]["height"] for line in lines]
    if not heights:
        return []
    reference_height = median(heights)
    titles = []
    for line in lines:
        word_count = line["word_count"]
        is_large = line["box"]["height"] >= reference_height * 1.25
        is_short = word_count <= 6
        if is_large and is_short:
            titles.append({"text": line["text"], "box": line["box"], "confidence": line["confidence"]})
    return titles


def group_sections(lines: list[dict[str, Any]], include_lines: bool = False) -> list[dict[str, Any]]:
    """Agrupa títulos com as linhas de texto visualmente relacionadas."""
    if not lines:
        return []

    heights = [line["box"]["height"] for line in lines]
    reference_height = median(heights)
    title_lines = {(line["text"], line["box"]["top"]) for line in lines
                   if line["box"]["height"] >= reference_height * 1.25 and line["word_count"] <= 6}

    columns: list[list[dict[str, Any]]] = []
    for line in lines:
        line_left = line["box"]["left"]
        target = next(
            (column for column in columns if abs(column[0]["box"]["left"] - line_left) <= 140),
            None,
        )
        if target is None:
            columns.append([line])
        else:
            target.append(line)

    sections: list[dict[str, Any]] = []
    for column in columns:
        ordered = sorted(column, key=lambda line: line["box"]["top"])
        current: list[dict[str, Any]] = []
        for line in ordered:
            is_title = (line["text"], line["box"]["top"]) in title_lines
            if current:
                previous = current[-1]
                gap = line["box"]["top"] - (previous["box"]["top"] + previous["box"]["height"])
                starts_new = is_title and gap > reference_height * 0.8
                too_far = gap > reference_height * 3.5
                if starts_new or too_far:
                    sections.append(_make_section(current, title_lines, include_lines))
                    current = []
            current.append(line)
        if current:
            sections.append(_make_section(current, title_lines, include_lines))

    return sorted(sections, key=lambda section: (section["box"]["top"], section["box"]["left"]))


def _make_section(lines: list[dict[str, Any]], title_lines: set[tuple[str, int]], include_lines: bool) -> dict[str, Any]:
    title_parts = [line["text"] for line in lines if (line["text"], line["box"]["top"]) in title_lines]
    title = " ".join(title_parts) if title_parts else None
    text_lines = [line["text"] for line in lines if (line["text"], line["box"]["top"]) not in title_lines]
    confidence = [line["confidence"] for line in lines if line["confidence"] >= 0]
    section = {
        "title": title,
        "text": " ".join(text_lines),
        "confidence": round(sum(confidence) / len(confidence), 2) if confidence else -1,
        "box": _lines_box(lines),
    }
    if include_lines:
        section["lines"] = lines
    return section
