import pytest

from mdfix.latex import LatexBracketNormalizer


# fmt: off
@pytest.mark.parametrize(
    "input_text,expected",
    [
        # 기본 케이스
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No LaTeX here", "No LaTeX here", id="no_latex"),  # LaTeX_없음

        # 기본 변환
        pytest.param("\\[ x^2 \\]", "$$x^2$$", id="simple_equation"),  # 간단한_수식
        pytest.param("\\[ a \\] and \\[ b \\]", "$$a$$ and $$b$$", id="multiple_equations"),  # 다중_수식
        pytest.param("\\[ x^2 + y^2 = z^2 \\]", "$$x^2 + y^2 = z^2$$", id="complex_equation"),  # 복잡한_수식

        # 공백 처리
        pytest.param("\\[x\\]", "$$x$$", id="no_spaces"),  # 공백_없음
        pytest.param("\\[ x \\]", "$$x$$", id="with_spaces"),  # 공백_제거
        pytest.param("\\[\nx^2\n\\]", "$$x^2$$", id="with_newlines"),  # 줄바꿈_제거

        # 텍스트 중간
        pytest.param("Text \\[ eq \\] more text", "Text $$eq$$ more text", id="inline_in_text"),  # 텍스트_중간_인라인

        # 일반 괄호는 변경 없음
        pytest.param("Regular [brackets]", "Regular [brackets]", id="regular_brackets_unchanged"),  # 일반_괄호_변경없음
    ],
)
# fmt: on
def test_latex_bracket_normalizer(input_text, expected):
    assert LatexBracketNormalizer()(input_text) == expected
