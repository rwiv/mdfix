import pytest

from mdfix.bullets import BulletIndentNormalizer


# fmt: off
@pytest.mark.parametrize(
    "input_text,expected",
    [
        # 기본 케이스
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No bullets here", "No bullets here", id="no_bullets"),  # 글머리_없음
        pytest.param("- Item", "- Item", id="no_indent_item"),  # 들여쓰기_없음

        # 들여쓰기 정규화 (2칸 -> 4칸)
        pytest.param("  - Item", "    - Item", id="2_space_to_4"),  # 2칸_4칸으로
        pytest.param("  - First\n  - Second", "    - First\n    - Second", id="multiple_2_space"),  # 다중_글머리_2칸

        # 이미 정규화된 경우 (4칸 유지)
        pytest.param("    - Item", "    - Item", id="4_space_unchanged"),  # 4칸_그대로
        pytest.param("    - First\n    - Second", "    - First\n    - Second", id="multiple_4_space"),  # 다중_글머리_4칸

        # 중첩 글머리
        pytest.param(
            "  - Level1\n    - Level2",
            "    - Level1\n        - Level2",
            id="nested_bullets",
        ),  # 중첩_글머리
        pytest.param(
            "  - Level1\n    - Level2\n      - Level3",
            "    - Level1\n        - Level2\n            - Level3",
            id="deeply_nested",
        ),  # 깊게_중첩

        # 다양한 글머리 타입
        pytest.param("  * Item", "    * Item", id="asterisk_2_space"),  # 별표_글머리
        pytest.param("  1. First\n  2. Second", "    1. First\n    2. Second", id="numbered_2_space"),  # 숫자_글머리
        pytest.param(
            "  - Item1\n  * Item2\n  1. Item3",
            "    - Item1\n    * Item2\n    1. Item3",
            id="mixed_bullet_types",
        ),  # 혼합_글머리_타입

        # 탭 변환
        pytest.param("\t- Item", "    - Item", id="tab_to_4_spaces"),  # 탭_공백_변환
        pytest.param("\t\t- Item", "        - Item", id="multiple_tabs"),  # 다중_탭

        # 글머리가 아닌 경우
        pytest.param("Text with - not bullet", "Text with - not bullet", id="dash_not_bullet"),  # 글머리_아님

        # min_indent가 0인 경우 중첩 글머리
        pytest.param(
            "- Item\n  - Nested",
            "- Item\n    - Nested",
            id="min_indent_zero",
        ),  # min_indent_0_중첩
    ],
)
# fmt: on
def test_bullet_indent_normalizer(input_text, expected):
    assert BulletIndentNormalizer()(input_text) == expected
