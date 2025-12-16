import re

from ..normalizer import Normalizer


class ReferenceMarkerNormalizer(Normalizer):
    """
    참고문헌 마커 형식을 정규화합니다.

    [숫자] 형식의 참고문헌 마커를 [^숫자] 형식(Markdown 각주)으로 변환한 후,
    [^숫자](URL)을 [^숫자]: URL 정의 형식으로 변환합니다.
    문서에서 참조되지 않는 참고문헌은 삭제됩니다.

    예시:
    - [1] → [^1]
    - [^1](used_ref) → [^1]: used_ref
    - [^2](unused_ref) → (문서에서 [^2]가 없으면 삭제)
    """

    def normalize(self, text: str) -> str:
        # 1단계: [숫자]를 [^숫자]로 변환
        text = re.sub(r"\[(\d+)\]", r"[^\1]", text)

        # 2단계: [^숫자](URL) 형식의 라인 처리 - 정의 형식으로 변환 또는 미사용시 삭제
        lines = text.split("\n")
        result_lines = []

        for i, line in enumerate(lines):
            match = re.match(r"\[\^(\d+)\]\((.*?)\)", line.strip())
            if not match:
                result_lines.append(line)
                continue

            # 참조 번호와 URL 추출
            ref_num = match.group(1)
            url = match.group(2)
            ref_marker = f"[^{ref_num}]"

            # 문서의 다른 곳에 참조가 존재하는지 확인
            other_lines = lines[:i] + lines[i + 1 :]
            other_text = "\n".join(other_lines)

            if ref_marker in other_text:
                # 참조가 존재하면 정의 형식으로 변환
                result_lines.append(f"[^{ref_num}]: {url}")

        return "\n".join(result_lines)
