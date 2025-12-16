from ..normalizer import Normalizer


class AsteriskNormalizer(Normalizer):
    """마크다운 리스트 형식을 별표에서 대시로 변환합니다.

    `*   ` (별표 + 공백 3개) 패턴을 `- ` (대시 + 공백)으로 변경합니다.
    """

    def normalize(self, text: str) -> str:
        return text.replace("*   ", "- ")
