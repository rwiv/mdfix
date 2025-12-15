import re


def remove_numbered_lines(content: str) -> str:
    """[숫자]로 시작하는 라인 전체를 제거합니다.

    [숫자] 다음 공백 유무와 관계없이 해당 라인을 찾아 제거합니다.

    Args:
        content: 변환할 원본 텍스트.

    Returns:
        str: [숫자]로 시작하는 라인이 제거된 텍스트.
    """
    return re.sub(r"^\[\d+\]\s*.*\n?", "", content, flags=re.MULTILINE)


def remove_numbered_brackets(content: str) -> str:
    """텍스트에서 공백 + [숫자] 패턴을 제거합니다.

    Args:
        content: 변환할 원본 텍스트.

    Returns:
        str: [숫자] 패턴이 제거된 텍스트.
    """
    return re.sub(r"\s*\[\d+\]", "", content)


def add_blank_line_after_headers(content: str) -> str:
    """마크다운 헤더 다음에 빈 줄이 없으면 추가합니다.

    헤더(#, ##, ### 등)와 다음 라인 사이에 개행이 1개만 있는 경우,
    2개로 늘려서 빈 줄을 추가합니다.

    Args:
        content: 변환할 원본 텍스트.

    Returns:
        str: 헤더 다음에 빈 줄이 추가된 텍스트.
    """
    return re.sub(r"^(#{1,6}\s+.+)\n(?=[^\n])", r"\1\n\n", content, flags=re.MULTILINE)


def normalize_header_levels(content: str) -> str:
    """문서의 헤더 레벨을 정규화합니다.

    - 최소 레벨이 1, 2면 그대로 냅둔다.
    - 최소 레벨이 3 이상이면 최소 레벨이 2가 되도록 모든 헤더의 레벨을 전체적으로 낮춘다.

    Args:
        content: 변환할 원본 텍스트.

    Returns:
        str: 헤더 레벨이 정규화된 텍스트.
    """
    # 모든 헤더 찾기
    header_pattern = re.compile(r"^(#{1,6})\s+", re.MULTILINE)
    headers = header_pattern.findall(content)

    if not headers:
        return content

    # 최소 헤더 레벨 찾기
    min_level = min(len(h) for h in headers)

    # 최소 레벨이 1 또는 2면 변경하지 않음
    if min_level <= 2:
        return content

    # 감소시킬 레벨 계산 (최소 레벨이 2가 되도록)
    reduce_by = min_level - 2

    # 모든 헤더 레벨 조정
    def adjust_header(match):
        hashes = match.group(1)
        new_level = len(hashes) - reduce_by
        return "#" * new_level + " "

    return header_pattern.sub(adjust_header, content)


def convert_latex_brackets_to_double_dollar(content: str) -> str:
    """LaTeX 수식 구분자를 마크다운 형식으로 변환합니다.

    \\[와 \\]를 $$로 변환하며, 구분자 주변의 불필요한 공백이나 개행을 제거합니다.
    - \\[ 뒤의 공백이나 개행 제거
    - \\] 앞의 공백이나 개행 제거

    Args:
        content: 변환할 원본 텍스트.

    Returns:
        str: LaTeX 수식 구분자가 $$로 변환된 텍스트.
    """
    # \[ 뒤의 공백이나 개행 제거하고 $$로 변환
    content = re.sub(r"\\\[[ \n]?", "$$", content)
    # \] 앞의 공백이나 개행 제거하고 $$로 변환
    content = re.sub(r"[ \n]?\\\]", "$$", content)
    return content


def convert_latex_parentheses_to_dollar(content: str) -> str:
    """LaTeX 인라인 수식 구분자를 마크다운 형식으로 변환합니다.

    \\(와 \\)를 $로 변환합니다.

    Args:
        content: 변환할 원본 텍스트.

    Returns:
        str: LaTeX 인라인 수식 구분자가 $로 변환된 텍스트.
    """
    # \(를 $로 변환
    content = content.replace("\\(", "$")
    # \)를 $로 변환
    content = content.replace("\\)", "$")
    return content


# TODO: add test
def remove_space_before_punctuation(content: str) -> str:
    """구두점 앞의 불필요한 공백을 제거합니다.

    문자 다음에 오는 공백 + 마침표 또는 콜론을
    문자 + 마침표/콜론으로 변환합니다.
    (예: "example ." -> "example.", "text :" -> "text:")

    Args:
        content: 변환할 원본 텍스트.

    Returns:
        str: 구두점 앞의 공백이 제거된 텍스트.
    """
    return re.sub(r"(\S)\s+([.:])", r"\1\2", content)


def convert_asterisk_to_dash(content: str) -> str:
    """마크다운 리스트 형식을 별표에서 대시로 변환합니다.

    *   (별표 + 공백 3개) 패턴을 - (대시 + 공백)로 변경합니다.

    Args:
        content: 변환할 원본 텍스트.

    Returns:
        str: 별표 리스트가 대시 리스트로 변환된 텍스트.
    """
    return content.replace("*   ", "- ")


def reduce_numbered_list_spaces(content: str) -> str:
    """번호 매긴 리스트의 공백을 정규화합니다.

    숫자. 다음의 공백 2개를 1개로 축소합니다 (예: 1.  foo -> 1. foo).

    Args:
        content: 변환할 원본 텍스트.

    Returns:
        str: 번호 매긴 리스트의 공백이 정규화된 텍스트.
    """
    return re.sub(r"(\d+\.)\s{2}", r"\1 ", content)
