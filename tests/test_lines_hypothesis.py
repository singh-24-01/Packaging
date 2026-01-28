from hypothesis import given, strategies as st

from ng20_lda.lines import count_lines_from_text


def expected_line_count(s: str) -> int:
    if s == "":
        return 0
    return s.count("\n") + (0 if s.endswith("\n") else 1)


@given(st.text())
def test_count_lines_property(s: str):
    assert count_lines_from_text(s) == expected_line_count(s)

