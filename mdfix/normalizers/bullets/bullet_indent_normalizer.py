import re
import sys

from ..normalizer import Normalizer


class BulletIndentNormalizer(Normalizer):
    """마크다운 글머리의 indent를 정규화합니다.

    모든 글머리(`-`, `*`, `1.` 등)의 최소 indent를 찾아서:
    - 최소 indent가 2라면 모든 글머리의 indent를 2배로 변환 (2 -> 4, 4 -> 8)
    - 최소 indent가 4라면 그대로 유지
    """

    def normalize(self, text: str) -> str:
        # 탭 문자를 스페이스로 변환
        text = _convert_tabs_to_spaces(text)

        # 글머리 패턴: 행 시작 + 공백 + (- 또는 * 또는 숫자.)
        bullet_pattern = re.compile(r"^( *)([-*]|\d+\.)", re.MULTILINE)

        # 모든 글머리와 indent 찾기
        matches = list(bullet_pattern.finditer(text))

        if not matches:
            return text

        # 모든 글머리의 indent 개수 추출
        min_indent = sys.maxsize
        for indent_len in [len(match.group(1)) for match in matches]:
            if indent_len == 0:
                continue
            if indent_len < min_indent:
                min_indent = indent_len

        if min_indent == sys.maxsize:
            return text

        # 최소 indent가 2라면 2배로 변환
        if min_indent == 2:
            return bullet_pattern.sub(_adjust_indent, text)

        return text


def _adjust_indent(match: re.Match[str]):
    spaces = match.group(1)
    new_spaces = " " * (len(spaces) * 2)
    bullet = match.group(2)
    return new_spaces + bullet


def _convert_tabs_to_spaces(text: str) -> str:
    """탭 문자를 스페이스로 변환합니다.

    모든 탭 문자(\t)를 4개의 스페이스로 변환합니다.
    """
    return text.replace("\t", "    ")
