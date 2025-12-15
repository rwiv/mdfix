import sys
import os
import re


def remove_numbered_lines(content: str) -> str:
    """[숫자]로 시작하는 라인 전체를 제거합니다.

    [숫자] 다음 공백 유무와 관계없이 해당 라인을 찾아 제거합니다.

    Args:
        content: 변환할 원본 텍스트.

    Returns:
        str: [숫자]로 시작하는 라인이 제거된 텍스트.
    """
    return re.sub(r'^\[\d+\]\s*.*\n?', '', content, flags=re.MULTILINE)


def remove_numbered_brackets(content: str) -> str:
    """텍스트에서 공백 + [숫자] 패턴을 제거합니다.

    Args:
        content: 변환할 원본 텍스트.

    Returns:
        str: [숫자] 패턴이 제거된 텍스트.
    """
    return re.sub(r'\s*\[\d+\]', '', content)



def convert_asterisk_to_dash(content: str) -> str:
    """마크다운 리스트 형식을 별표에서 대시로 변환합니다.

    *   (별표 + 공백 3개) 패턴을 - (대시 + 공백)로 변경합니다.

    Args:
        content: 변환할 원본 텍스트.

    Returns:
        str: 별표 리스트가 대시 리스트로 변환된 텍스트.
    """
    return content.replace('*   ', '- ')


def reduce_numbered_list_spaces(content: str) -> str:
    """번호 매긴 리스트의 공백을 정규화합니다.

    숫자. 다음의 공백 2개를 1개로 축소합니다 (예: 1.  foo -> 1. foo).

    Args:
        content: 변환할 원본 텍스트.

    Returns:
        str: 번호 매긴 리스트의 공백이 정규화된 텍스트.
    """
    return re.sub(r'(\d+\.)\s{2}', r'\1 ', content)


def add_blank_line_after_headers(content: str) -> str:
    """마크다운 헤더 다음에 빈 줄이 없으면 추가합니다.

    헤더(#, ##, ### 등)와 다음 라인 사이에 개행이 1개만 있는 경우,
    2개로 늘려서 빈 줄을 추가합니다.

    Args:
        content: 변환할 원본 텍스트.

    Returns:
        str: 헤더 다음에 빈 줄이 추가된 텍스트.
    """
    return re.sub(r'^(#{1,6}\s+.+)\n(?=[^\n])', r'\1\n\n', content, flags=re.MULTILINE)


def normalize_header_levels(content: str) -> str:
    """문서의 헤더 레벨을 정규화하여 최대 레벨을 2로 제한합니다.

    문서에서 사용된 헤더의 최대 레벨이 3 이상인 경우,
    모든 헤더 레벨을 조정하여 최대 레벨이 2가 되도록 합니다.
    최대 레벨이 1 또는 2인 경우 변경하지 않습니다.

    Args:
        content: 변환할 원본 텍스트.

    Returns:
        str: 헤더 레벨이 정규화된 텍스트.
    """
    # 모든 헤더 찾기
    header_pattern = re.compile(r'^(#{1,6})\s+', re.MULTILINE)
    headers = header_pattern.findall(content)

    if not headers:
        return content

    # 최대 헤더 레벨 찾기
    max_level = max(len(h) for h in headers)

    # 최대 레벨이 2 이하면 변경하지 않음
    if max_level <= 2:
        return content

    # 감소시킬 레벨 계산
    reduce_by = max_level - 2

    # 모든 헤더 레벨 조정
    def adjust_header(match):
        hashes = match.group(1)
        new_level = max(1, len(hashes) - reduce_by)  # 최소 레벨 1 유지
        return '#' * new_level + ' '

    return header_pattern.sub(adjust_header, content)


def convert_latex_brackets_to_double_dollar(content: str) -> str:
    """LaTeX 수식 구분자를 마크다운 형식으로 변환합니다.

    \[와 \]를 $$로 변환하며, 구분자 주변의 불필요한 공백이나 개행을 제거합니다.
    - \[ 뒤의 공백이나 개행 제거
    - \] 앞의 공백이나 개행 제거

    Args:
        content: 변환할 원본 텍스트.

    Returns:
        str: LaTeX 수식 구분자가 $$로 변환된 텍스트.
    """
    # \[ 뒤의 공백이나 개행 제거하고 $$로 변환
    content = re.sub(r'\\\[[ \n]?', '$$', content)
    # \] 앞의 공백이나 개행 제거하고 $$로 변환
    content = re.sub(r'[ \n]?\\\]', '$$', content)
    return content


def convert_latex_parentheses_to_dollar(content: str) -> str:
    """LaTeX 인라인 수식 구분자를 마크다운 형식으로 변환합니다.

    \(와 \)를 $로 변환합니다.

    Args:
        content: 변환할 원본 텍스트.

    Returns:
        str: LaTeX 인라인 수식 구분자가 $로 변환된 텍스트.
    """
    # \(를 $로 변환
    content = content.replace('\\(', '$')
    # \)를 $로 변환
    content = content.replace('\\)', '$')
    return content


def get_paths():
    """커맨드 라인 인자로부터 파일 경로 목록을 가져옵니다.

    Returns:
        list[str]: 커맨드 라인 인자로 전달된 파일 경로 목록.
                   인자가 없으면 빈 리스트 반환.
    """
    if len(sys.argv) < 2:
        return []

    # 드래그된 모든 파일의 경로 가져오기
    return sys.argv[1:]


def apply_transformations(content: str, mode: str = 'default') -> str:
    """mode에 따라 다른 변환 전략을 적용합니다.

    Args:
        content: 변환할 원본 텍스트.
        mode: 변환 모드 ('mode1', 'mode2', 'default' 등).

    Returns:
        str: 변환된 텍스트.
    """
    # mode별 변환 함수 목록 정의
    transformations = {
        'mode1': [
            remove_numbered_lines,
            remove_numbered_brackets,
            convert_asterisk_to_dash,
            reduce_numbered_list_spaces,
        ],
        'mode2': [
            add_blank_line_after_headers,
            normalize_header_levels,
            convert_latex_brackets_to_double_dollar,
            convert_latex_parentheses_to_dollar,
        ],
        'default': [
            remove_numbered_lines,
            remove_numbered_brackets,
            convert_asterisk_to_dash,
            reduce_numbered_list_spaces,
            add_blank_line_after_headers,
            normalize_header_levels,
            convert_latex_brackets_to_double_dollar,
            convert_latex_parentheses_to_dollar,
        ],
    }

    # 해당 mode의 변환 함수들을 순차적으로 적용
    funcs = transformations.get(mode, transformations['default'])
    for func in funcs:
        content = func(content)

    return content


def conv_md(paths: list[str], mode: str = 'default'):
    """마크다운 파일들을 변환하여 _out 접미사를 가진 새 파일로 저장합니다.

    Args:
        paths: 변환할 마크다운 파일 경로 목록.
        mode: 변환 모드 ('mode1', 'mode2', 'default' 등).
    """
    if not paths:
        return

    for source_path in paths:
        # 원본 파일 읽기
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # mode에 따른 변환 작업
        content = apply_transformations(content, mode)

        # 출력 파일 경로 생성 (원본과 같은 디렉터리에 _out 붙임)
        dir_name = os.path.dirname(source_path)
        base_name = os.path.basename(source_path)
        name, ext = os.path.splitext(base_name)
        output_path = os.path.join(dir_name, f"{name}_out{ext}")

        # 변환된 내용 저장
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    conv_md(get_paths())
