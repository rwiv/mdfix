import re

from ..normalizer import Normalizer


class HeaderLineBreakAdder(Normalizer):
    """마크다운 헤더 다음에 빈 줄이 없으면 추가합니다.

    헤더(#, ##, ### 등)와 다음 라인 사이에 개행이 1개만 있는 경우,
    2개로 늘려서 빈 줄을 추가합니다.
    """

    def normalize(self, text: str) -> str:
        return re.sub(r"^(#{1,6} +.+)\n(?=[^\n])", r"\1\n\n", text, flags=re.MULTILINE)
