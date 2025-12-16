import re

from ..normalizer import Normalizer


class ReferenceMarkerRemover(Normalizer):
    """텍스트에서 공백 + [숫자] 패턴을 제거합니다."""

    def normalize(self, text: str) -> str:
        return re.sub(r" *\[\d+\] *", "", text)
