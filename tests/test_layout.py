from c3pocr.layout import detect_titles, group_blocks, group_lines, group_sections


def word(text, left, top, width=20, height=10, line_num=1, block_num=1):
    return {
        "text": text,
        "left": left,
        "top": top,
        "width": width,
        "height": height,
        "confidence": 95.0,
        "block_num": block_num,
        "par_num": 1,
        "line_num": line_num,
    }


def test_group_words_into_lines_and_blocks():
    lines = group_lines([
        word("Valor", 10, 10),
        word("Total", 40, 10),
        word("89,90", 150, 10),
        word("Dia", 10, 30, line_num=2),
    ])

    assert [line["text"] for line in lines] == ["Valor Total 89,90", "Dia"]
    assert group_blocks(lines)[0]["text"] == "Valor Total 89,90\nDia"


def test_detect_large_short_lines_as_titles():
    lines = group_lines([
        word("Company", 10, 10, height=30),
        word("Overview", 80, 10, width=40, height=30),
        word("Texto", 10, 60, height=10, line_num=2),
    ])

    assert detect_titles(lines)[0]["text"] == "Company Overview"


def test_group_title_and_body_into_section():
    lines = group_lines([
        word("Company", 10, 10, height=30),
        word("Overview", 80, 10, width=40, height=30),
        word("Insert", 10, 70, height=10, line_num=2),
        word("desired", 70, 70, width=40, height=10, line_num=2),
        word("text", 120, 70, height=10, line_num=2),
    ])

    sections = group_sections(lines)

    assert sections[0]["title"] == "Company Overview"
    assert sections[0]["text"] == "Insert desired text"


def test_split_large_horizontal_gap_into_separate_lines():
    lines = group_lines([
        word("Company", 10, 10, height=30),
        word("Our", 300, 10, height=30),
    ])

    assert [line["text"] for line in lines] == ["Company", "Our"]
