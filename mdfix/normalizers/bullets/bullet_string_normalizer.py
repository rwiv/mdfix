import re

from .bullet_regex import BULLET_PATTERN
from ..normalizer import Normalizer


class BulletStringNormalizer(Normalizer):
    """
    모든 종류의 리스트 형식의 글머리를 정규화합니다.

    글머리 형식과 공백을 다음과 같이 정규화합니다:
    - `*`, `+` → `-`로 통일
    - `1)` → `1.`로 통일
    - 글머리 뒤의 공백을 1개로 정규화
    - 기존 들여쓰기는 유지

    예: `* foo` → `- foo`, `+ bar` → `- bar`, `1) baz` → `1. baz`
    """

    def normalize(self, text: str) -> str:
        # 글머리 패턴: 행 시작 + 공백 + (*, -, 숫자., 숫자)) + 공백(n개)
        bullet_pattern = re.compile(BULLET_PATTERN, re.MULTILINE)
        # 글머리 뒤의 공백을 1개로 정규화 + bullet 정규화 + 기존 들여쓰기는 유지
        return bullet_pattern.sub(_replace_bullet, text)


def _replace_bullet(match: re.Match[str]):
    indent = match.group(1)
    bullet = match.group(2)
    # * → -
    bullet = bullet.replace("*", "-")
    bullet = bullet.replace("+", "-")
    # ) → .
    bullet = bullet.replace(")", ".")
    return f"{indent}{bullet} "
