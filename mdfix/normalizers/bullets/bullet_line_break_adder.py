import re

from .bullet_regex import BULLET_PATTERN
from ..normalizer import Normalizer


class BulletLineBreakAdder(Normalizer):
    """
    글머리 기호 위에 빈 줄을 추가합니다.

    not글머리 라인이 바로 앞에 있고 비어있지 않은 경우, 글머리 기호 앞에 빈 줄을 추가합니다.
    예: 본문 텍스트 다음에 글머리 기호가 오면 그 사이에 빈 줄을 삽입합니다.
    """

    def normalize(self, text: str) -> str:
        lines = text.split("\n")
        result = []

        for i, line in enumerate(lines):
            if re.match(BULLET_PATTERN, line) and i > 0:
                prev_line = lines[i - 1]
                prev_stripped = prev_line.strip()
                prev_is_bullet = re.match(BULLET_PATTERN, prev_line)

                # 이전 라인이 글머리 라인이 아니고 비어있지 않으면 빈 줄 추가
                if not prev_is_bullet and prev_stripped != "":
                    result.append("")

            result.append(line)

        return "\n".join(result)
