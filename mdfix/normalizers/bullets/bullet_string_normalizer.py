import re

from ..normalizer import Normalizer


class BulletStringNormalizer(Normalizer):
    """모든 종류의 리스트 형식의 공백을 정규화합니다.

    `*`, `-`, `숫자.`, `숫자)` 등 다양한 글머리 형식 다음의 공백을 1개로 정규화합니다.
    예: `* foo`, `- foo`, `1. foo`, `1) foo` 등
    기존 들여쓰기는 유지됩니다.
    """

    def normalize(self, text: str) -> str:
        # 글머리 패턴: 행 시작 + 공백 + (*, -, 숫자., 숫자)) + 공백(n개)
        bullet_pattern = re.compile(r"^( *)([*\-]|\d+[.)])( +)", re.MULTILINE)
        # 글머리 뒤의 공백을 1개로 정규화 + bullet 정규화 + 기존 들여쓰기는 유지
        return bullet_pattern.sub(_replace_bullet, text)


def _replace_bullet(match: re.Match[str]):
    indent = match.group(1)
    bullet = match.group(2)
    # * → -
    bullet = bullet.replace("*", "-")
    # ) → .
    bullet = bullet.replace(")", ".")
    return f"{indent}{bullet} "
