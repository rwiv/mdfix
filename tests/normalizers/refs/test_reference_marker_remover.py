import pytest

from mdfix.normalizers.refs import ReferenceMarkerRemover


@pytest.mark.parametrize(
    "input_text,expected",
    [
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No brackets here", "No brackets here", id="no_brackets"),  # 괄호_없음
        pytest.param("Citation [1]", "Citation", id="single_bracket"),  # 단일_괄호
        pytest.param("Text [1] more [2]", "Text more", id="multiple_brackets"),  # 다중_괄호
        pytest.param("Space  [1]  test", "Space  test", id="with_spaces"),  # 공백_포함
        pytest.param("Multi [123] digit", "Multi digit", id="multi_digit"),  # 여러_자리수
        pytest.param("[1] Start", " Start", id="line_start"),  # 줄_시작
        pytest.param("End [999]", "End", id="line_end"),  # 줄_끝
        pytest.param("[abc] not removed", "[abc] not removed", id="not_numeric"),  # 숫자_아님
        pytest.param("Mixed [1] and [abc]", "Mixed and [abc]", id="mixed_brackets"),  # 혼합_괄호
        pytest.param("No space[1]", "No space", id="no_leading_space"),  # 앞_공백_없음
        pytest.param(" [1] [2] [3]", "", id="consecutive_brackets"),  # 연속된_여러_괄호
    ],
)
def test_reference_marker_remover(input_text, expected):
    assert ReferenceMarkerRemover()(input_text) == expected
