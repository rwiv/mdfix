import re

from ..normalizer import Normalizer


class MultipleNewlinesRemover(Normalizer):
    """
    3개 이상의 연속된 개행을 2개의 개행으로 변환한다.

    예시: "text\n\n\n\n\n\nmore" -> "text\n\nmore"
    """

    def normalize(self, text: str) -> str:
        return re.sub(r"\n{3,}", "\n\n", text)
