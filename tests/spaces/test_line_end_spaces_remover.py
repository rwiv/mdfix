import pytest

from mdfix.spaces import LineEndSpacesRemover


@pytest.mark.parametrize(
    "input_text,expected",
    # fmt: off
    [
        # 기본 케이스
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No trailing spaces", "No trailing spaces", id="no_trailing_spaces"),  # 줄_끝_공백_없음

        # 줄 끝 공백 제거
        pytest.param("hello.    ", "hello.", id="single_trailing_spaces"),  # 단일_줄_끝_공백
        pytest.param("hello   \nworld", "hello\nworld", id="first_line_trailing"),  # 첫_줄_끝_공백

        # 다중 줄
        pytest.param(
            "  hello   \n  world  ",
            "  hello\n  world",
            id="multiple_lines_trailing",
        ),  # 다중_줄_끝_공백

        # 앞의 공백 유지
        pytest.param("  hello  ", "  hello", id="preserve_leading_spaces"),  # 앞의_공백_유지
        pytest.param("    text    ", "    text", id="leading_and_trailing"),  # 앞뒤_공백

        # 중간 공백은 유지
        pytest.param("  hello  world  ", "  hello  world", id="middle_spaces_preserved"),  # 중간_공백_유지
    ],
    # fmt: on
)
def test_line_end_spaces_remover(input_text, expected):
    assert LineEndSpacesRemover()(input_text) == expected
