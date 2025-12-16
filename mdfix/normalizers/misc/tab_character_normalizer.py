from ..normalizer import Normalizer


class TabCharacterNormalizer(Normalizer):
    """탭 문자를 스페이스로 변환합니다.

    모든 탭 문자(\t)를 4개의 스페이스로 변환합니다.
    """

    def normalize(self, text: str) -> str:
        return text.replace("\t", "    ")
