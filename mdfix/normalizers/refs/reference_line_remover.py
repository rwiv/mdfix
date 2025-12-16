import re

from ..normalizer import Normalizer


class ReferenceLineRemover(Normalizer):
    """[숫자]로 시작하는 라인 전체를 제거합니다.

    [숫자] 다음 공백 유무와 관계없이 해당 라인을 찾아 제거합니다.
    """

    def normalize(self, text: str) -> str:
        return re.sub(r"^\[\d+\] *.*\n?", "", text, flags=re.MULTILINE)
