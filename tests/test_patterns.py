from c3pocr.patterns import parse_lines


def test_parse_common_document_lines():
    result = parse_lines("Valor Total .................... 89,90\nDia ............................ 19/03")
    assert result["valor_total"]["value"] == 89.90
    assert result["data"]["value"] == "19/03"


def test_ignore_unknown_lines():
    assert parse_lines("Cliente .................... Ana") == {}
