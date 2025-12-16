import re

from ..normalizer import Normalizer


class HeaderLevelNormalizer(Normalizer):
    """문서의 헤더 레벨을 정규화합니다.

    - 최소 레벨이 1, 2면 그대로 냅둔다.
    - 최소 레벨이 3 이상이면 최소 레벨이 2가 되도록 모든 헤더의 레벨을 전체적으로 낮춘다.
    """

    def normalize(self, text: str) -> str:
        # 모든 헤더 찾기
        header_pattern = re.compile(r"^(#{1,6})\s+", re.MULTILINE)
        headers = header_pattern.findall(text)

        if not headers:
            return text

        # 최소 헤더 레벨 찾기
        min_level = min(len(h) for h in headers)

        # 최소 레벨이 1 또는 2면 변경하지 않음
        if min_level <= 2:
            return text

        # 감소시킬 레벨 계산 (최소 레벨이 2가 되도록)
        reduce_by = min_level - 2

        # 모든 헤더 레벨 조정
        def adjust_header(match: re.Match[str]):
            hashes = match.group(1)
            new_level = len(hashes) - reduce_by
            return "#" * new_level + " "

        return header_pattern.sub(adjust_header, text)
