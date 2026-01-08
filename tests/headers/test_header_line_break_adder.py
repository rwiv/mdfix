import pytest

from mdfix.headers import HeaderLineBreakAdder


@pytest.mark.parametrize(
    "input_text,expected",
    # fmt: off
    [
        # 기본 케이스
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No headers here", "No headers here", id="no_headers"),  # 헤더_없음

        # 헤더 뒤 빈 줄 추가 (모든 레벨)
        pytest.param("## H2\nText", "## H2\n\nText", id="h2_no_blank_line"),  # h2_빈줄_없음
        pytest.param("### H3\nText", "### H3\n\nText", id="h3_no_blank_line"),  # h3_빈줄_없음
        pytest.param("#### H4\nText", "#### H4\n\nText", id="h4_no_blank_line"),  # h4_빈줄_없음
        pytest.param("##### H5\nText", "##### H5\n\nText", id="h5_no_blank_line"),  # h5_빈줄_없음
        pytest.param("###### H6\nText", "###### H6\n\nText", id="h6_no_blank_line"),  # h6_빈줄_없음

        # 1레벨은 스킵
        pytest.param("# H1\nText", "# H1\nText", id="h1_no_blank_line"),  # h1_레벨_빈줄_없음

        # 이미 빈 줄이 있는 경우
        pytest.param("## H2\n\nText", "## H2\n\nText", id="already_has_blank_line"),  # 이미_빈줄_있음
        pytest.param("## H2\n\n\nText", "## H2\n\n\nText", id="multiple_blank_lines"),  # 여러_빈줄

        # 다중 헤더
        pytest.param("## H2\n### H3\nText", "## H2\n\n### H3\n\nText", id="consecutive_headers"),  # 연속된_헤더

        # 끝에 헤더
        pytest.param("# End header", "# End header", id="header_at_end"),  # 끝에_헤더
    ],
    # fmt: on
)
def test_header_line_break_adder(input_text, expected):
    assert HeaderLineBreakAdder()(input_text) == expected
