import pytest

from mdfix.normalizers.misc import HorizontalBarRemover


@pytest.mark.parametrize(
    "input_text,expected",
    # fmt: off
    [
        # 기본 케이스
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No horizontal bars", "No horizontal bars", id="no_horizontal_bars"),  # 수평선_없음

        # 기본 수평선 (Dash)
        pytest.param("---", "", id="dash_three"),  # 대시_3개
        pytest.param("-----", "", id="dash_five"),  # 대시_5개

        # 기본 수평선 (Asterisk)
        pytest.param("***", "", id="asterisk_three"),  # 별표_3개
        pytest.param("*****", "", id="asterisk_five"),  # 별표_5개

        # 공백이 포함된 수평선
        pytest.param("- - -", "", id="dash_with_spaces"),  # 대시_공백_포함
        pytest.param("* * *", "", id="asterisk_with_spaces"),  # 별표_공백_포함

        # 들여쓰기된 수평선
        pytest.param("  ---", "", id="indented_horizontal_bar"),  # 들여쓰기_수평선

        # 수평선이 아닌 경우 (조건 미충족)
        pytest.param("--", "--", id="dash_two"),  # 대시_2개_미충족
        pytest.param("**", "**", id="asterisk_two"),  # 별표_2개_미충족
        pytest.param("--- text", "--- text", id="dash_with_text"),  # 대시_텍스트_포함
        pytest.param("*** text", "*** text", id="asterisk_with_text"),  # 별표_텍스트_포함

        # 콘텐츠 사이 수평선
        pytest.param(
            "Text\n---\nMore text",
            "Text\n\nMore text",
            id="horizontal_bar_between_content",
        ),  # 콘텐츠_사이_수평선
        pytest.param(
            "Text\n\n---\n\nMore text",
            "Text\n\nMore text",
            id="horizontal_bar_with_empty_lines",
        ),  # 빈줄_사이_수평선

        # 시작과 끝
        pytest.param("---\nText", "\nText", id="horizontal_bar_at_start"),  # 시작_수평선
        pytest.param("Text\n---", "Text\n", id="horizontal_bar_at_end"),  # 끝_수평선

        # 연속된 수평선
        pytest.param(
            "Text\n\n---\n\n***\n\nEnd",
            "Text\n\nEnd",
            id="consecutive_horizontal_bars",
        ),  # 연속_수평선

        # 복합 시나리오
        pytest.param(
            "Header\n\n---\n\nParagraph 1\n\n---\nParagraph 2\n---\n\nEnd",
            "Header\n\nParagraph 1\n\nParagraph 2\n\nEnd",
            id="complex_scenario",
        ),  # 복합_시나리오
    ],
    # fmt: on
)
def test_horizontal_bar_remover(input_text, expected):
    assert HorizontalBarRemover()(input_text) == expected
