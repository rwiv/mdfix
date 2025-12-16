import pytest

from mdfix.normalizers.refs import ReferenceLineRemover


@pytest.mark.parametrize(
    "input_text,expected",
    # fmt: off
    [
        # 기본 케이스
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No numbered lines", "No numbered lines", id="no_numbered_lines"),  # 번호_줄_없음

        # 단일 번호 줄 제거
        pytest.param("[1] Remove this\n", "", id="single_numbered_line"),  # 단일_번호_줄

        # 다중 번호 줄
        pytest.param("[1] First\n[2] Second\n", "", id="multiple_numbered_lines"),  # 다중_번호_줄
        pytest.param("[1]\n[2]\n[3]\n", "", id="consecutive_numbers"),  # 연속된_번호

        # 위치별 테스트
        pytest.param("[1] Start\nKeep", "Keep", id="number_at_start"),  # 시작에_번호
        pytest.param("Keep\n[1] End", "Keep\n", id="number_at_end"),  # 끝에_번호
        pytest.param("Keep\n[1] Middle\nKeep", "Keep\nKeep", id="number_in_middle"),  # 중간에_번호

        # 다양한 번호
        pytest.param("[123] Multi digit\n", "", id="multi_digit_number"),  # 여러_자리_번호
        pytest.param("[1]No space after\n", "", id="no_space_after_bracket"),  # 공백_없음

        # 줄 시작이 아닌 경우
        pytest.param("Not [1] at start", "Not [1] at start", id="not_at_line_start"),  # 줄_시작_아님
    ],
    # fmt: on
)
def test_reference_line_remover(input_text, expected):
    assert ReferenceLineRemover()(input_text) == expected
