import pytest

from mdfix.normalizers.misc import LineEndSpacesRemover


@pytest.mark.parametrize(
    "input_text,expected",
    [
        # fmt: off
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("hello.", "hello.", id="no_trailing_spaces"),  # 줄_끝_공백_없음
        pytest.param("hello.    ", "hello.", id="trailing_spaces"),  # 줄_끝_공백_제거
        pytest.param("  hello  ", "  hello", id="preserve_leading_spaces"),  # 앞의_공백_유지
        pytest.param("hello   \nworld", "hello\nworld", id="first_line_trailing_spaces"),  # 첫_줄_끝_공백
        pytest.param("  hello   \n  world  ", "  hello\n  world", id="multiple_lines_trailing_spaces"),  # 다중_줄_끝_공백
        pytest.param("  hello  world  ", "  hello  world", id="middle_spaces_preserved"),
        # 혼합_공백
        # fmt: on
    ],
)
def test_line_end_spaces_remover(input_text, expected):
    assert LineEndSpacesRemover()(input_text) == expected
