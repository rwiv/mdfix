import sys
import os

from mdfix.normalizers import Normalizer, bullets, headers, latex, refs, misc


def get_argv_paths() -> list[str]:
    """커맨드 라인 인자로부터 파일 경로 목록을 가져옵니다.

    Returns:
        list[str]: 커맨드 라인 인자로 전달된 파일 경로 목록.
                   인자가 없으면 빈 리스트 반환.
    """
    if len(sys.argv) < 2:
        return []

    # 드래그된 모든 파일의 경로 가져오기
    return sys.argv[1:]


def normalize(content: str, mode: str = "default") -> str:
    """mode에 따라 다른 변환 전략을 적용합니다.

    Args:
        content: 변환할 원본 텍스트.
        mode: 변환 모드.

    Returns:
        str: 변환된 텍스트.
    """
    # mode별 변환 함수 목록 정의
    norms: dict[str, list[Normalizer]] = {
        "remove_refs_gemini": [
            refs.ReferenceLineRemover(),  # refs.ReferenceMarkerRemover 보다 먼저 시행 필요
            refs.ReferenceMarkerRemover(),
            latex.LatexBracketNormalizer(),
            latex.LatexParenthesisNormalizer(),
            misc.TabCharacterNormalizer(),  # bullets.BulletIndentNormalizer 보다 먼저 시행 필요
            misc.HorizontalBarRemover(),
            headers.HeaderEmphasisRemover(),
            headers.HeaderLevelNormalizer(),
            headers.HeaderLineBreakAdder(),
            headers.HeaderNumberMarkerConverter(delimiter=")"),
            bullets.BulletIndentNormalizer(),
            bullets.BulletStringNormalizer(),
            bullets.BulletLineBreakAdder(),
            misc.LineEndSpacesRemover(),
        ],
    }

    if mode == "default":
        mode = "remove_refs_gemini"

    # 해당 mode의 변환 함수들을 순차적으로 적용
    funcs = norms[mode]
    for func in funcs:
        content = func(content)

    return content


def normalize_md(paths: list[str], mode: str = "default"):
    """마크다운 파일들을 변환하여 _out 접미사를 가진 새 파일로 저장합니다.

    Args:
        paths: 변환할 마크다운 파일 경로 목록.
        mode: 변환 모드.
    """
    if not paths:
        return

    for source_path in paths:
        # 원본 파일 읽기
        with open(source_path, "r", encoding="utf-8") as f:
            content = f.read()

        # mode에 따른 변환 작업
        content = normalize(content, mode)

        # 출력 파일 경로 생성 (원본과 같은 디렉터리에 _out 붙임)
        dir_name = os.path.dirname(source_path)
        base_name = os.path.basename(source_path)
        name, ext = os.path.splitext(base_name)
        output_path = os.path.join(dir_name, f"{name}_out{ext}")

        # 변환된 내용 저장
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
