import pytest

from mdfix.normalizers.bullets import BulletIndentNormalizer


@pytest.mark.parametrize(
    "input_text,expected",
    [
        # fmt: off
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No bullets here", "No bullets here", id="no_bullets"),  # 글머리_없음
        pytest.param("- Item", "- Item", id="single_bullet_no_indent"),  # 단일_글머리_들여쓰기_없음
        pytest.param("  - Item", "    - Item", id="single_bullet_2_space_indent"),  # 단일_글머리_2칸
        pytest.param("  - First\n  - Second", "    - First\n    - Second", id="multiple_bullets_2_space"),  # 다중_글머리_2칸
        pytest.param("    - Item", "    - Item", id="single_bullet_4_space_indent"),  # 단일_글머리_4칸
        pytest.param(
            "    - First\n    - Second",
            "    - First\n    - Second",
            id="multiple_bullets_4_space",
        ),  # 다중_글머리_4칸
        pytest.param(
            "  - Level1\n    - Level2",
            "    - Level1\n        - Level2",
            id="nested_bullets_2_and_4",
        ),  # 중첩_글머리
        pytest.param("  * Item", "    * Item", id="asterisk_bullet_2_space"),  # 별표_글머리_2칸
        pytest.param(
            "  1. First\n  2. Second",
            "    1. First\n    2. Second",
            id="numbered_bullets_2_space",
        ),  # 숫자_글머리_2칸
        pytest.param(
            "  - Item1\n  * Item2\n  1. Item3",
            "    - Item1\n    * Item2\n    1. Item3",
            id="mixed_bullet_types_2_space",
        ),  # 혼합_글머리_2칸
        pytest.param("\t- Item", "    - Item", id="tab_to_spaces"),  # 탭_스페이스_변환
        pytest.param("\t\t- Item", "        - Item", id="multiple_tabs"),  # 다중_탭
        pytest.param(
            "  - Level1\n    - Level2\n      - Level3",
            "    - Level1\n        - Level2\n            - Level3",
            id="deeply_nested",
        ),  # 깊게_중첩
        pytest.param("Text with - not bullet", "Text with - not bullet", id="dash_not_bullet"),  # 대시_글머리_아님
        pytest.param(
            "  - Item with text\n  - Another",
            "    - Item with text\n    - Another",
            id="bullets_with_text",
        ),  # 텍스트가_있는_글머리
        pytest.param(
            "- Item with text\n  - Another",
            "- Item with text\n    - Another",
            id="min_indent_zero_with_nested",
        ),
        # min_indent가_0인_경우_중첩_글머리
        # fmt: on
    ],
)
def test_bullet_indent_normalizer(input_text, expected):
    assert BulletIndentNormalizer()(input_text) == expected
