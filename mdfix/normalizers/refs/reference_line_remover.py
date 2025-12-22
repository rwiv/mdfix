import re

from ..normalizer import Normalizer


class ReferenceLineRemover(Normalizer):
    """
    "[숫자] "로 시작하는 라인 전체를 제거합니다.
    """

    def normalize(self, text: str) -> str:
        return re.sub(r"^\[\d+\] *.*\n?", "", text, flags=re.MULTILINE)
