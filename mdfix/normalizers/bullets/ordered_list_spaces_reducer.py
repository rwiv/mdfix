import re

from ..normalizer import Normalizer


class OrderedListSpacesReducer(Normalizer):
    """번호 매긴 리스트의 공백을 정규화합니다.

    `숫자+.` 다음의 공백 2개를 1개로 축소합니다 (예: 1.  foo -> 1. foo).
    """

    def normalize(self, text: str) -> str:
        return re.sub(r"(\d+\.)\s{2}", r"\1 ", text)
