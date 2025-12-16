import pytest

from mdfix.normalizers.bullets import AsteriskNormalizer


@pytest.mark.parametrize(
    "input_text,expected",
    [
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No asterisks", "No asterisks", id="no_asterisks"),  # 별표_없음
        pytest.param("*   Item", "- Item", id="single_item"),  # 단일_항목
        pytest.param("*   First\n*   Second", "- First\n- Second", id="multiple_items"),  # 다중_항목
        pytest.param("* Item", "* Item", id="one_space"),  # 공백_1개
        pytest.param("*  Item", "*  Item", id="two_spaces"),  # 공백_2개
        pytest.param("*    Item", "-  Item", id="four_spaces"),  # 공백_4개
        pytest.param("Text * not list", "Text * not list", id="not_a_list"),  # 별표_목록_아님
        pytest.param("*   Level 1\n    *   Level 2", "- Level 1\n    - Level 2", id="nested_list"),  # 중첩_목록
        pytest.param("*   Multiple *   patterns", "- Multiple - patterns", id="multiple_patterns"),  # 다중_패턴
    ],
)
def test_asterisk_normalizer(input_text, expected):
    assert AsteriskNormalizer()(input_text) == expected
