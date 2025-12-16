import pytest

from mdfix.normalizers.bullets import OrderedListSpacesReducer


@pytest.mark.parametrize(
    "input_text,expected",
    [
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No numbered lists", "No numbered lists", id="no_numbered_lists"),  # 번호_목록_없음
        pytest.param("1.  Item", "1. Item", id="single_item"),  # 단일_항목
        pytest.param("1.  First\n2.  Second", "1. First\n2. Second", id="multiple_items"),  # 다중_항목
        pytest.param("1. Already normalized", "1. Already normalized", id="already_normalized"),  # 이미_정규화됨
        pytest.param("10.  Double digit", "10. Double digit", id="double_digit"),  # 두_자리수
        pytest.param("999.  Triple digit", "999. Triple digit", id="triple_digit"),  # 세_자리수
        pytest.param("1.   Three spaces", "1.  Three spaces", id="three_spaces"),  # 공백_3개
        pytest.param("Mixed 1.  and 2. formats", "Mixed 1. and 2. formats", id="mixed_spacing"),  # 혼합_간격
    ],
)
def test_ordered_list_spaces_reducer(input_text, expected):
    assert OrderedListSpacesReducer()(input_text) == expected
