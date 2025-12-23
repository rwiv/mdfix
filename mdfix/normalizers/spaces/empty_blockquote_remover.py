import re

from ..normalizer import Normalizer


class EmptyBlockquoteRemover(Normalizer):
    """
    빈 blockquote를 제거합니다
    """

    def normalize(self, text: str) -> str:
        return re.sub(r"^> *\n", "", text, flags=re.MULTILINE)
