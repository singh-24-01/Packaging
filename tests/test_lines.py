import tempfile
from pathlib import Path

from ng20_lda.lines import count_lines_from_path, count_lines_from_text


def test_count_lines_from_text_basic():
    assert count_lines_from_text("") == 0
    assert count_lines_from_text("one line") == 1
    assert count_lines_from_text("a\nb\n") == 2
    assert count_lines_from_text("a\nb") == 2


def test_count_lines_from_path_tempfile():
    with tempfile.NamedTemporaryFile() as tmp:
        p = Path(tmp.name)
        tmp.write(b"a\nb\n")
        tmp.flush()
        assert count_lines_from_path(p) == 2

