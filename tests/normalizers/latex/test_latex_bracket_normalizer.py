import pytest

from mdfix.normalizers.latex import LatexBracketNormalizer


@pytest.mark.parametrize(
    "input_text,expected",
    [
        # fmt: off
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
        pytest.param("Text \\[ eq \\] more text", "Text $$eq$$ more text", id="inline_in_text"),
        # 텍스트_중간_인라인
        # fmt: on
    ],
)
def test_convert_latex_brackets_to_double_dollar_cases(input_text, expected):
    assert LatexBracketNormalizer()(input_text) == expected
