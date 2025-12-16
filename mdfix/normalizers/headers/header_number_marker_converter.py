import re

from ..normalizer import Normalizer


class HeaderNumberMarkerConverter(Normalizer):
    """마크다운 헤더의 원형 숫자 기호를 일반 숫자로 변환합니다.

    헤더 내의 ①, ②, ③ 등의 원형 숫자를 일반 숫자로 변환합니다.
    (예: "## ① hello" -> "## 1) hello", "## ② world" -> "## 2. world")
    """

    # fmt: off
    # 원형 숫자를 일반 숫자로 매핑
    __circled_to_number = {
        "①": "1", "②": "2", "③": "3", "④": "4", "⑤": "5",
        "⑥": "6", "⑦": "7", "⑧": "8", "⑨": "9", "⑩": "10",
        "⑪": "11", "⑫": "12", "⑬": "13", "⑭": "14", "⑮": "15",
        "⑯": "16", "⑰": "17", "⑱": "18", "⑲": "19", "⑳": "20",
    }
    # fmt: on

    def __init__(self, delimiter: str = ")") -> None:
        """
        Args:
            delimiter: 숫자 뒤의 구분자 (기본값: ")", "."도 가능)
        """
        super().__init__()
        self.delimiter = delimiter

    def normalize(self, text: str) -> str:
        return re.sub(r"^(#{1,6}) +(.+)$", self.__convert_circled, text, flags=re.MULTILINE)

    def __convert_circled(self, match: re.Match[str]):
        header_marker = match.group(1)  # #, ##, ### 등
        header_text = match.group(2)  # 헤더 텍스트

        # 원형 숫자를 일반 숫자로 변환
        for circled, number in self.__circled_to_number.items():
            header_text = header_text.replace(circled, number + self.delimiter)

        return header_marker + " " + header_text
