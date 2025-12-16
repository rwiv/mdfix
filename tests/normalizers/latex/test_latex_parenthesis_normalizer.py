import pytest

from mdfix.normalizers.latex import LatexParenthesisNormalizer


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
    assert LatexParenthesisNormalizer()(input_text) == expected
