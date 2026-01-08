import re

from ..normalizer import Normalizer


class ReferenceMarkerRemover(Normalizer):
    """텍스트에서 공백 + [숫자] 패턴을 제거합니다."""

    def normalize(self, text: str) -> str:
        # 그룹 1: 코드 블록 (fenced code block)
        # 그룹 2: 코드 블록의 fence (``` 또는 ~~~)
        # 그룹 3: Reference Marker (공백 + [숫자] + 공백)
        pattern = r"(^(`{3,}|~{3,}).*?^\2)|( *\[\d+\] *)"

        def replacement(match):
            if match.group(1):
                return match.group(1)  # 코드 블록은 그대로 유지
            return ""  # Reference Marker는 제거

        return re.sub(pattern, replacement, text, flags=re.MULTILINE | re.DOTALL)
