import pytest
import re

from pyscript.conv_md.trans import (
    remove_numbered_brackets,
    remove_numbered_lines,
    convert_asterisk_to_dash,
    reduce_numbered_list_spaces,
    add_blank_line_after_headers,
    normalize_header_levels,
    convert_latex_brackets_to_double_dollar,
    convert_latex_parentheses_to_dollar,
    remove_space_before_punctuation,
)


@pytest.mark.parametrize(
    "input_text,expected",
    [
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No brackets here", "No brackets here", id="no_brackets"),  # 괄호_없음
        pytest.param("Citation [1]", "Citation", id="single_bracket"),  # 단일_괄호
        pytest.param("Text [1] more [2]", "Text more", id="multiple_brackets"),  # 다중_괄호
        pytest.param("Space  [1]  test", "Space  test", id="with_spaces"),  # 공백_포함
        pytest.param("Multi [123] digit", "Multi digit", id="multi_digit"),  # 여러_자리수
        pytest.param("[1] Start", " Start", id="line_start"),  # 줄_시작
        pytest.param("End [999]", "End", id="line_end"),  # 줄_끝
        pytest.param("[abc] not removed", "[abc] not removed", id="not_numeric"),  # 숫자_아님
        pytest.param("Mixed [1] and [abc]", "Mixed and [abc]", id="mixed_brackets"),  # 혼합_괄호
        pytest.param("No space[1]", "No space", id="no_leading_space"),  # 앞_공백_없음
        pytest.param(" [1] [2] [3]", "", id="consecutive_brackets"),  # 연속된_여러_괄호
    ],
)
def test_remove_numbered_brackets_cases(input_text, expected):
    assert remove_numbered_brackets(input_text) == expected


@pytest.mark.parametrize(
    "input_text,expected",
    [
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No numbered lines", "No numbered lines", id="no_numbered_lines"),  # 번호_줄_없음
        pytest.param("[1] Remove this\n", "", id="single_numbered_line"),  # 단일_번호_줄
        pytest.param("[1] First\n[2] Second\n", "", id="multiple_numbered_lines"),  # 다중_번호_줄
        pytest.param("Keep\n[1] Remove\nKeep", "Keep\nKeep", id="number_in_middle"),  # 중간에_번호
        pytest.param("[1] Start\nKeep", "Keep", id="number_at_start"),  # 시작에_번호
        pytest.param("Keep\n[1] End", "Keep\n", id="number_at_end"),  # 끝에_번호
        pytest.param("[1]\n[2]\n[3]\n", "", id="consecutive_numbers"),  # 연속된_번호
        pytest.param("Not [1] at start", "Not [1] at start", id="not_at_line_start"),  # 줄_시작_아님
        pytest.param("[123] Multi digit\n", "", id="multi_digit_number"),  # 여러_자리_번호
        pytest.param("[1]No space after\n", "", id="no_space_after_bracket"),  # 괄호_뒤_공백_없음
    ],
)
def test_remove_numbered_lines_cases(input_text, expected):
    assert remove_numbered_lines(input_text) == expected


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
def test_convert_asterisk_to_dash_cases(input_text, expected):
    assert convert_asterisk_to_dash(input_text) == expected


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
def test_reduce_numbered_list_spaces_cases(input_text, expected):
    assert reduce_numbered_list_spaces(input_text) == expected


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
    assert add_blank_line_after_headers(input_text) == expected


@pytest.mark.parametrize(
    "input_text,expected",
    [
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No headers", "No headers", id="no_headers"),  # 헤더_없음
        pytest.param("# H1\n## H2", "# H1\n## H2", id="min_level_1_no_change_a"),  # 최소레벨1_변경없음_a
        pytest.param("# H1", "# H1", id="min_level_1_no_change_b"),  # 최소레벨1_변경없음_b
        pytest.param("### H3", "## H3", id="h3_alone_to_h2"),  # h3_단독_h2로
        pytest.param("#### H4", "## H4", id="h4_alone_to_h2"),  # h4_단독_h2로
        pytest.param("# H1\n### H3", "# H1\n### H3", id="min_level_1_no_change_mixed"),  # 최소레벨1_변경없음_혼합
        pytest.param("## H2\n#### H4", "## H2\n#### H4", id="min_level_2_no_change"),  # 최소레벨2_변경없음
        pytest.param(
            "### H3\n#### H4\n##### H5", "## H3\n### H4\n#### H5", id="all_levels_normalized"
        ),  # 모든_레벨_정규화됨
    ],
)
def test_normalize_header_levels_cases(input_text, expected):
    result = normalize_header_levels(input_text)
    assert result == expected

    # Verify min level is at most 2
    header_pattern = re.compile(r"^(#{1,6})\s+", re.MULTILINE)
    headers = header_pattern.findall(result)
    if headers:
        min_level = min(len(h) for h in headers)
        assert min_level <= 2, f"Min level should be <= 2, got {min_level}"


@pytest.mark.parametrize(
    "input_text,expected",
    [
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No LaTeX here", "No LaTeX here", id="no_latex"),  # LaTeX_없음
        pytest.param("\\[ x^2 \\]", "$$x^2$$", id="simple_equation"),  # 간단한_수식
        pytest.param("\\[ a \\] and \\[ b \\]", "$$a$$ and $$b$$", id="multiple_equations"),  # 다중_수식
        pytest.param("\\[ x^2 + y^2 = z^2 \\]", "$$x^2 + y^2 = z^2$$", id="complex_equation"),  # 복잡한_수식
        pytest.param("\\[\nx^2\n\\]", "$$x^2$$", id="with_newlines"),  # 줄바꿈_포함
        pytest.param("\\[x\\]", "$$x$$", id="no_spaces"),  # 공백_없음
        pytest.param("\\[ x\\]", "$$x$$", id="space_after_opening"),  # 여는_괄호_뒤_공백
        pytest.param("\\[x \\]", "$$x$$", id="space_before_closing"),  # 닫는_괄호_앞_공백
        pytest.param("Regular [brackets]", "Regular [brackets]", id="regular_brackets_unchanged"),  # 일반_괄호_변경없음
        pytest.param("Text \\[ eq \\] more text", "Text $$eq$$ more text", id="inline_in_text"),  # 텍스트_중간_인라인
    ],
)
def test_convert_latex_brackets_to_double_dollar_cases(input_text, expected):
    assert convert_latex_brackets_to_double_dollar(input_text) == expected


@pytest.mark.parametrize(
    "input_text,expected",
    [
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No LaTeX here", "No LaTeX here", id="no_latex"),  # LaTeX_없음
        pytest.param("\\(x\\)", "$x$", id="simple_inline"),  # 간단한_인라인
        pytest.param("\\(a\\) and \\(b\\)", "$a$ and $b$", id="multiple_inline"),  # 다중_인라인
        pytest.param("Text \\(x^2\\) more", "Text $x^2$ more", id="inline_in_text"),  # 텍스트_중간_인라인
        pytest.param("\\(a + b = c\\)", "$a + b = c$", id="equation_inline"),  # 수식_인라인
        pytest.param("Regular (parentheses)", "Regular (parentheses)", id="regular_parens_unchanged"),  # 일반_괄호_변경없음
        pytest.param("\\(\\(nested\\)\\)", "$$nested$$", id="nested_parens"),  # 중첩된_괄호
        pytest.param("Mix \\(inline\\) and (regular)", "Mix $inline$ and (regular)", id="mixed_parens"),  # 혼합_괄호
    ],
)
def test_convert_latex_parentheses_to_dollar_cases(input_text, expected):
    assert convert_latex_parentheses_to_dollar(input_text) == expected


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
    assert remove_space_before_punctuation(input_text) == expected
