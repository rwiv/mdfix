import pytest

from mdfix.normalizers.refs import ReferenceMarkerRemover


@pytest.mark.parametrize(
    "input_text,expected",
    [
        # fmt: off
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No brackets here", "No brackets here", id="no_brackets"),  # 괄호_없음
        pytest.param("a [1] b  [2]", "ab", id="multiple_brackets"),  # 다중_괄호
        pytest.param("Multi [123]", "Multi", id="multi_digit"),  # 여러_자리수
        pytest.param("[1] Start", "Start", id="line_start"),  # 줄_시작
        pytest.param("[abc] not removed", "[abc] not removed", id="not_numeric"),  # 숫자_아님
        pytest.param("Mixed [1] [abc]", "Mixed[abc]", id="mixed_brackets"),  # 혼합_괄호
        pytest.param(" [1] [2] [3]", "", id="consecutive_brackets"),  # 연속된_여러_괄호
        pytest.param("hello. [1]", "hello.", id="single_bracket"),  # 단일_괄호
        pytest.param("hello[1] .", "hello.", id="no_space_before_bracket"),  # 공백_없이_대괄호
        pytest.param("hello [1].", "hello.", id="space_before_bracket_punct_after"),  # 공백_뒤_대괄호_구두점_붙어있음
        pytest.param("hello [1] .", "hello.", id="space_before_and_after_bracket"),
        # 공백_뒤_대괄호_공백_후_구두점
        # fmt: on
    ],
)
def test_reference_marker_remover(input_text, expected):
    assert ReferenceMarkerRemover()(input_text) == expected
