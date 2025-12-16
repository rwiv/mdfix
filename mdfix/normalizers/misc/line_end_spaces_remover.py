from ..normalizer import Normalizer


class LineEndSpacesRemover(Normalizer):
    """각 줄의 끝에 있는 공백을 제거합니다.

    마크다운 텍스트의 모든 줄 끝에 있는 불필요한 공백들을 제거합니다.
    예: `hello.    ` -> `hello.`
    """

    def normalize(self, text: str) -> str:
        lines = text.split("\n")
        return "\n".join(line.rstrip() for line in lines)
