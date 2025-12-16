import re

from ..normalizer import Normalizer


class PunctuationSpaceRemover(Normalizer):
    """구두점 앞의 불필요한 공백을 제거합니다.

    문자 다음에 오는 공백 + 마침표 또는 콜론을
    문자 + 마침표/콜론으로 변환합니다.
    (예: "example ." -> "example.", "text :" -> "text:")
    """

    def normalize(self, text: str) -> str:
        return re.sub(r"(\S)\s+([.:])", r"\1\2", text)
