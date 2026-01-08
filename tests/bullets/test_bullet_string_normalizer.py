import pytest

from mdfix.bullets import BulletStringNormalizer


@pytest.mark.parametrize(
    "input_text,expected",
    # fmt: off
    [
        # 기본 케이스
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No bullet lists", "No bullet lists", id="no_bullet_lists"),  # 글머리_없음

        # Asterisk (*) 테스트 (* → -)
        pytest.param("*  Item", "- Item", id="asterisk_with_spaces"),  # 별표_공백_정규화

        # Dash (-) 테스트
        pytest.param("-  Item", "- Item", id="dash_with_spaces"),  # 대시_공백_정규화

        # Numbered dot (숫자.) 테스트
        pytest.param("1.  Item", "1. Item", id="numbered_dot_with_spaces"),  # 번호점_공백_정규화

        # Numbered parenthesis (숫자)) 테스트 () → .)
        pytest.param("1)  Item", "1. Item", id="numbered_paren_with_spaces"),  # 번호괄호_변환

        # 다중 항목 (혼합 마커)
        pytest.param(
            "*  First\n-  Second\n1.  Third\n1)  Fourth",
            "- First\n- Second\n1. Third\n1. Fourth",
            id="mixed_markers",
        ),  # 혼합_마커

        # 중첩 목록
        pytest.param(
            "*   Level 1\n  -   Level 2",
            "- Level 1\n  - Level 2",
            id="nested_list",
        ),  # 중첩_목록

        # 들여쓰기
        pytest.param("  *  Item", "  - Item", id="indented_asterisk"),  # 들여쓰기_별표
        pytest.param("    -  Item", "    - Item", id="indented_dash"),  # 들여쓰기_대시
        pytest.param("  12.  Item", "  12. Item", id="indented_numbered_dot"),  # 들여쓰기_번호점
        pytest.param("    1)  Item", "    1. Item", id="indented_numbered_paren"),  # 들여쓰기_번호괄호

        # 이미 정규화된 항목
        pytest.param("* Item", "- Item", id="already_normalized_asterisk"),  # 이미_정규화됨_별표
        pytest.param("- Item", "- Item", id="already_normalized_dash"),  # 이미_정규화됨_대시
        pytest.param("1. Item", "1. Item", id="already_normalized_numbered_dot"),  # 이미_정규화됨_번호점
        pytest.param("1) Item", "1. Item", id="already_normalized_numbered_paren"),  # 이미_정규화됨_번호괄호

        # 마크다운이 아닌 일반 텍스트
        pytest.param("Text * not list", "Text * not list", id="asterisk_not_at_line_start"),  # 별표_줄시작_아님
        pytest.param("Text - not list", "Text - not list", id="dash_not_at_line_start"),  # 대시_줄시작_아님
        pytest.param("Text 1. not list", "Text 1. not list", id="numbered_dot_not_at_line_start"),  # 번호점_줄시작_아님
    ],
    # fmt: on
)
def test_bullet_string_normalizer(input_text, expected):
    assert BulletStringNormalizer()(input_text) == expected
