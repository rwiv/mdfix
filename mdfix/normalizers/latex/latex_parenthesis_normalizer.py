from ..normalizer import Normalizer


class LatexParenthesisNormalizer(Normalizer):
    """LaTeX 인라인 수식 구분자를 마크다운 형식으로 변환합니다.

    \\(와 \\)를 $로 변환합니다.
    """

    def normalize(self, text: str) -> str:
        # \(를 $로 변환
        text = text.replace("\\(", "$")
        # \)를 $로 변환
        text = text.replace("\\)", "$")
        return text
