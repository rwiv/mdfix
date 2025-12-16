import re

from ..normalizer import Normalizer


class HeaderEmphasisRemover(Normalizer):
    """마크다운 헤더의 강조 표시를 제거합니다.

    헤더 내의 **bold**, *italic*, _emphasis_ 같은 강조 표시를 제거합니다.
    (예: "## **hello**" -> "## hello", "### _world_" -> "### world")
    """

    def normalize(self, text: str) -> str:
        return re.sub(r"^(#{1,6})\s+(.+)$", _remove_emphasis, text, flags=re.MULTILINE)


def _remove_emphasis(match: re.Match[str]):
    header_marker = match.group(1)  # #, ##, ### 등
    header_text = match.group(2)  # 헤더 텍스트
    # 강조 표시 제거: *, _ 문자 제거
    cleaned_text = re.sub(r"[*_]+", "", header_text)
    return header_marker + " " + cleaned_text
