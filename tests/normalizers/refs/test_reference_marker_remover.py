import pytest

from mdfix.normalizers.refs import ReferenceMarkerRemover


@pytest.mark.parametrize(
    "input_text,expected",
    # fmt: off
    [
        # 기본 케이스
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No brackets here", "No brackets here", id="no_brackets"),  # 괄호_없음

        # 숫자 괄호 제거
        pytest.param("[1] Start", "Start", id="bracket_at_line_start"),  # 줄_시작_괄호
        pytest.param("hello. [1]", "hello.", id="bracket_at_end"),  # 끝_괄호
        pytest.param("a [1] b", "ab", id="bracket_in_middle"),  # 중간_괄호
        pytest.param("a [1] b  [2]", "ab", id="multiple_brackets"),  # 다중_괄호

        # 다양한 번호
        pytest.param("Multi [123]", "Multi", id="multi_digit"),  # 여러_자리수
        pytest.param(" [1] [2] [3]", "", id="consecutive_brackets"),  # 연속된_여러_괄호

        # 공백 처리
        pytest.param("hello[1] .", "hello.", id="no_space_before_bracket"),  # 공백_없이_대괄호
        pytest.param("hello [1].", "hello.", id="bracket_before_punct"),  # 괄호_구두점_앞
        pytest.param("hello [1] .", "hello.", id="bracket_with_space"),  # 괄호_양옆_공백

        # 비숫자 괄호는 제거 안 함
        pytest.param("[abc] not removed", "[abc] not removed", id="not_numeric"),  # 숫자_아님
        pytest.param("Mixed [1] [abc]", "Mixed[abc]", id="mixed_brackets"),  # 혼합_괄호
    ],
    # fmt: on
)
def test_reference_marker_remover(input_text, expected):
    assert ReferenceMarkerRemover()(input_text) == expected
