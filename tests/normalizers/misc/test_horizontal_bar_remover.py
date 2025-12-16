import pytest

from mdfix.normalizers.misc import HorizontalBarRemover


@pytest.mark.parametrize(
    "input_text,expected",
    [
        # fmt: off
        # 기본 케이스
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No horizontal bars", "No horizontal bars", id="no_horizontal_bars"),  # 수평선_없음

        # Dash (-) 수평선 테스트
        pytest.param("---", "", id="dash_three"),  # 대시_3개
        pytest.param("-----", "", id="dash_five"),  # 대시_5개
        pytest.param("- - -", "", id="dash_with_spaces"),  # 대시_공백_포함

        # Asterisk (*) 수평선 테스트
        pytest.param("***", "", id="asterisk_three"),  # 별표_3개
        pytest.param("*****", "", id="asterisk_five"),  # 별표_5개
        pytest.param("* * *", "", id="asterisk_with_spaces"),  # 별표_공백_포함

        # 위 아래 빈 줄 있는 경우 (아래 빈 줄도 제거)
        pytest.param(
            "Text\n\n---\n\nMore text",
            "Text\n\nMore text",
            id="horizontal_bar_between_empty_lines"
        ),  # 수평선_위아래_빈줄_사이

        # 위 아래 모두 내용 있는 경우
        pytest.param(
            "Text\n---\nMore text",
            "Text\n\nMore text",
            id="horizontal_bar_between_content"
        ),  # 수평선_위아래_내용_사이

        # 들여쓰기된 수평선
        pytest.param("  ---", "", id="indented_horizontal_bar"),  # 들여쓰기_수평선

        # 수평선 조건을 만족하지 않는 경우
        pytest.param("--", "--", id="dash_two"),  # 대시_2개
        pytest.param("**", "**", id="asterisk_two"),  # 별표_2개
        pytest.param("--- text", "--- text", id="dash_with_text"),  # 대시_텍스트_포함
        pytest.param("*** text", "*** text", id="asterisk_with_text"),  # 별표_텍스트_포함

        # 시작과 끝에 위치한 수평선
        pytest.param("---\nText", "\nText", id="horizontal_bar_at_start"),  # 수평선_시작
        pytest.param("Text\n---", "Text\n", id="horizontal_bar_at_end"),  # 수평선_끝
        pytest.param("---\n\nText", "\nText", id="horizontal_bar_at_start_with_below_empty"),  # 수평선_시작_아래_빈줄

        # 연속된 수평선
        pytest.param(
            "Text\n\n---\n\n***\n\nEnd",
            "Text\n\nEnd",
            id="consecutive_horizontal_bars"
        ),  # 연속_수평선

        # 복합 시나리오
        pytest.param(
            "Header\n\n---\n\nParagraph 1\n\n---\nParagraph 2\n---\n\nEnd",
            "Header\n\nParagraph 1\n\nParagraph 2\n\nEnd",
            id="complex_scenario"
        ),
        # 복합_시나리오
        # fmt: on
    ],
)
def test_horizontal_bar_remover(input_text, expected):
    assert HorizontalBarRemover()(input_text) == expected
