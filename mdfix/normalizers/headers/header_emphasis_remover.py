import re

from ..normalizer import Normalizer


class HeaderEmphasisRemover(Normalizer):
    """
    마크다운 헤더의 강조 표시를 제거합니다.

    헤더 내의 **bold**, *italic*, _emphasis_ 같은 강조 표시를 제거합니다.
    (예: "## **hello**" -> "## hello", "### _world_" -> "### world")
    """

    def normalize(self, text: str) -> str:
        return re.sub(r"^(#{1,6}) +(.+)$", _remove_emphasis, text, flags=re.MULTILINE)


def _remove_emphasis(match: re.Match[str]):
    header_marker = match.group(1)  # #, ##, ### 등
    header_text = match.group(2)  # 헤더 텍스트
    # 재귀적으로 emphasis 패턴 제거
    prev = None
    while prev != header_text:
        prev = header_text
        # **bold** 제거
        header_text = re.sub(r"\*\*(.+?)\*\*", r"\1", header_text)
        # __bold__ 제거
        header_text = re.sub(r"__(.+?)__", r"\1", header_text)
        # *italic* 제거
        header_text = re.sub(r"\*(.+?)\*", r"\1", header_text)
        # _italic_ 제거
        header_text = re.sub(r"_(.+?)_", r"\1", header_text)
    return header_marker + " " + header_text
