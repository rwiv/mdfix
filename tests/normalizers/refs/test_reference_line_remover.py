import pytest

from mdfix.normalizers.refs import ReferenceLineRemover


@pytest.mark.parametrize(
    "input_text,expected",
    [
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No numbered lines", "No numbered lines", id="no_numbered_lines"),  # 번호_줄_없음
        pytest.param("[1] Remove this\n", "", id="single_numbered_line"),  # 단일_번호_줄
        pytest.param("[1] First\n[2] Second\n", "", id="multiple_numbered_lines"),  # 다중_번호_줄
        pytest.param("Keep\n[1] Remove\nKeep", "Keep\nKeep", id="number_in_middle"),  # 중간에_번호
        pytest.param("[1] Start\nKeep", "Keep", id="number_at_start"),  # 시작에_번호
        pytest.param("Keep\n[1] End", "Keep\n", id="number_at_end"),  # 끝에_번호
        pytest.param("[1]\n[2]\n[3]\n", "", id="consecutive_numbers"),  # 연속된_번호
        pytest.param("Not [1] at start", "Not [1] at start", id="not_at_line_start"),  # 줄_시작_아님
        pytest.param("[123] Multi digit\n", "", id="multi_digit_number"),  # 여러_자리_번호
        pytest.param("[1]No space after\n", "", id="no_space_after_bracket"),  # 괄호_뒤_공백_없음
    ],
)
def test_reference_line_remover(input_text, expected):
    assert ReferenceLineRemover()(input_text) == expected
