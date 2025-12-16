import pytest

from mdfix.normalizers.headers import HeaderLineBreakAdder


@pytest.mark.parametrize(
    "input_text,expected",
    [
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No headers here", "No headers here", id="no_headers"),  # 헤더_없음
        pytest.param("# H1\nText", "# H1\n\nText", id="h1_no_blank_line"),  # h1_빈줄_없음
        pytest.param("## H2\nText", "## H2\n\nText", id="h2_no_blank_line"),  # h2_빈줄_없음
        pytest.param("### H3\nText", "### H3\n\nText", id="h3_no_blank_line"),  # h3_빈줄_없음
        pytest.param("#### H4\nText", "#### H4\n\nText", id="h4_no_blank_line"),  # h4_빈줄_없음
        pytest.param("##### H5\nText", "##### H5\n\nText", id="h5_no_blank_line"),  # h5_빈줄_없음
        pytest.param("###### H6\nText", "###### H6\n\nText", id="h6_no_blank_line"),  # h6_빈줄_없음
        pytest.param("# H1\n\nText", "# H1\n\nText", id="already_has_blank_line"),  # 이미_빈줄_있음
        pytest.param("# H1\n## H2\nText", "# H1\n\n## H2\n\nText", id="consecutive_headers"),  # 연속된_헤더
        pytest.param("# End header", "# End header", id="header_at_end"),  # 끝에_헤더
        pytest.param("# H1\n\n\nText", "# H1\n\n\nText", id="multiple_blank_lines"),  # 여러_빈줄
    ],
)
def test_add_blank_line_after_headers_cases(input_text, expected):
    assert HeaderLineBreakAdder()(input_text) == expected
