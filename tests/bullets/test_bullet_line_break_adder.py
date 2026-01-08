import pytest

from mdfix.bullets import BulletLineBreakAdder


@pytest.mark.parametrize(
    "input_text,expected",
    # fmt: off
    [
        # 기본 케이스
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No bullets here", "No bullets here", id="no_bullets"),  # 글머리_없음
        pytest.param("- Item", "- Item", id="first_line_is_bullet"),  # 첫_줄이_글머리

        # 빈 줄 추가 케이스 - 일반 텍스트 다음에 글머리
        pytest.param("Text\n- Item", "Text\n\n- Item", id="text_then_bullet"),  # 텍스트_다음_글머리
        pytest.param("Some content\n- First\n- Second", "Some content\n\n- First\n- Second", id="content_then_multiple_bullets"),  # 내용_다음_여러_글머리

        # 빈 줄 추가하지 않는 케이스 - 글머리 다음에 글머리
        pytest.param("- First\n- Second", "- First\n- Second", id="bullet_then_bullet"),  # 글머리_다음_글머리
        pytest.param("- First\n- Second\n- Third", "- First\n- Second\n- Third", id="consecutive_bullets"),  # 연속_글머리

        # 빈 줄이 이미 있는 경우
        pytest.param("Text\n\n- Item", "Text\n\n- Item", id="blank_line_already_exists"),  # 빈_줄_이미_존재

        # 다양한 글머리 타입
        pytest.param("Text\n* Item", "Text\n\n* Item", id="asterisk_bullet"),  # 별표_글머리
        pytest.param("Text\n+ Item", "Text\n\n+ Item", id="plus_bullet"),  # 플러스_글머리
        pytest.param("Text\n1. Item", "Text\n\n1. Item", id="numbered_bullet"),  # 번호_글머리
        pytest.param("Text\n2) Item", "Text\n\n2) Item", id="parenthesis_bullet"),  # 괄호_글머리

        # 들여쓰기가 있는 글머리
        pytest.param("Text\n  - Item", "Text\n\n  - Item", id="indented_bullet"),  # 들여쓰기_글머리
        pytest.param("Text\n    - Item\n    - Item2", "Text\n\n    - Item\n    - Item2", id="indented_consecutive_bullets"),  # 들여쓰기_연속_글머리

        # 복합 케이스
        pytest.param(
            "Introduction\n- Point 1\n- Point 2\nConclusion\n- Note",
            "Introduction\n\n- Point 1\n- Point 2\nConclusion\n\n- Note",
            id="multiple_sections",
        ),  # 다중_섹션

        # 비어있는 이전 줄에는 추가하지 않음
        pytest.param("Text\n\n- Item", "Text\n\n- Item", id="empty_prev_line"),  # 빈_이전_줄

        # 글머리가 아닌 줄 (패턴 미매치)
        pytest.param("- Not a bullet at all", "- Not a bullet at all", id="dash_not_at_start"),  # 글머리_아님
        pytest.param("Text with - dash", "Text with - dash", id="dash_in_middle"),  # 중간_대시
    ],
    # fmt: on
)
def test_bullet_line_break_adder(input_text, expected):
    assert BulletLineBreakAdder()(input_text) == expected
