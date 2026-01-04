import re

from ..normalizer import Normalizer


class PaddingLineRemover(Normalizer):
    """
    padding line을 제거합니다.

    padding line은 4개 이상의 공백 문자만으로 구성된 줄을 의미합니다.
    중간의 빈 줄(blank line)은 보존됩니다.

    단, 코드 블록(``` 또는 ~~~) 내부에 있는 padding line은 제거하지 않습니다.

    예시:
    - ``"    \\nbar\\n    "`` -> ``"bar\\n"`` (양쪽의 4개 공백 줄 제거)
    - ``"  \\nfoo\\n\\nbar\\n"`` -> ``"  \\nfoo\\n\\nbar\\n"`` (2개 공백은 제거되지 않음)
    """

    def normalize(self, text: str) -> str:
        # 그룹 1: 코드 블록 (fenced code block)
        # 그룹 2: 코드 블록의 fence (``` 또는 ~~~)
        # 그룹 3: Padding line (4개 이상의 공백으로 시작하는 줄)
        pattern = r"(^(`{3,}|~{3,}).*?^\2)|(^ {4,}\n)"

        def replacement(match):
            if match.group(1):
                return match.group(1)  # 코드 블록은 그대로 유지
            return ""  # Padding line은 제거

        return re.sub(pattern, replacement, text, flags=re.MULTILINE | re.DOTALL)
