import pytest

from mdfix.normalizers.spaces import PunctuationSpaceRemover


@pytest.mark.parametrize(
    "input_text,expected",
    [
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No punctuation here", "No punctuation here", id="no_punctuation"),  # 구두점_없음
        pytest.param("example .", "example.", id="period_with_space"),  # 마침표_앞_공백
        pytest.param("text :", "text:", id="colon_with_space"),  # 콜론_앞_공백
        pytest.param("example  .", "example.", id="period_with_double_space"),  # 마침표_앞_공백_2개
        pytest.param("text   :", "text:", id="colon_with_triple_space"),  # 콜론_앞_공백_3개
        pytest.param("first . second :", "first. second:", id="multiple_punctuation"),  # 다중_구두점
        pytest.param("already.", "already.", id="already_normalized_period"),  # 이미_정규화됨_마침표
        pytest.param("already:", "already:", id="already_normalized_colon"),  # 이미_정규화됨_콜론
        pytest.param("both . and :", "both. and:", id="both_period_and_colon"),  # 마침표와_콜론_모두
        pytest.param("example, comma", "example, comma", id="comma_unchanged"),  # 쉼표_변경없음
        pytest.param("example ; semicolon", "example ; semicolon", id="semicolon_unchanged"),  # 세미콜론_변경없음
        pytest.param("mixed . text : here", "mixed. text: here", id="mixed_text"),  # 혼합_텍스트
        pytest.param("tab\t.", "tab.", id="tab_before_period"),  # 탭_다음_마침표
        pytest.param("newline\n.", "newline.", id="newline_before_period"),  # 줄바꿈_다음_마침표
    ],
)
def test_remove_space_before_punctuation_cases(input_text, expected):
    assert PunctuationSpaceRemover()(input_text) == expected
