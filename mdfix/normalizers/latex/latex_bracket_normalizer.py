import re

from ..normalizer import Normalizer


class LatexBracketNormalizer(Normalizer):
    """LaTeX 수식 구분자를 마크다운 형식으로 변환합니다.

    \\[와 \\]를 $$로 변환하며, 구분자 주변의 불필요한 공백이나 개행을 제거합니다.
    - \\[ 뒤의 공백이나 개행 제거
    - \\] 앞의 공백이나 개행 제거
    """

    def normalize(self, text: str) -> str:
        # \[ 뒤의 공백이나 개행 제거하고 $$로 변환
        text = re.sub(r"\\\[[ \n]?", "$$", text)
        # \] 앞의 공백이나 개행 제거하고 $$로 변환
        text = re.sub(r"[ \n]?\\\]", "$$", text)
        return text
