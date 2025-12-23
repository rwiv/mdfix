import re

from ..normalizer import Normalizer


class PaddingLineRemover(Normalizer):
    """
    padding line을 제거합니다.

    padding line은 4개 이상의 공백 문자만으로 구성된 줄을 의미합니다.
    중간의 빈 줄(blank line)은 보존됩니다.

    예시:
    - ``"    \\nbar\\n    "`` -> ``"bar\\n"`` (양쪽의 4개 공백 줄 제거)
    - ``"  \\nfoo\\n\\nbar\\n"`` -> ``"  \\nfoo\\n\\nbar\\n"`` (2개 공백은 제거되지 않음)
    """

    def normalize(self, text: str) -> str:
        return re.sub(r"^ {4,}\n", "", text, flags=re.MULTILINE)
