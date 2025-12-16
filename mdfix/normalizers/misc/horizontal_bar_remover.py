from ..normalizer import Normalizer


class HorizontalBarRemover(Normalizer):
    """
    Markdown의 horizontal bar를 제거합니다.

    Horizontal bar(---, ***, 등)의 처리 규칙:
    - 위와 아래가 모두 빈 줄인 경우: 위의 빈 줄과 horizontal bar를 모두 제거
    - 위 또는 아래 중 하나만 빈 줄인 경우: horizontal bar만 제거
    - 위와 아래가 모두 빈 줄이 아닌 경우: horizontal bar를 빈 줄로 대체
    """

    def normalize(self, text: str) -> str:
        lines = text.split("\n")
        result_lines = []

        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # 빈 줄인 경우 그대로 추가
            if not stripped:
                result_lines.append(line)
                i += 1
                continue

            # horizontal bar인지 확인 (- 또는 *로 시작하고 _is_horizontal_bar 조건 만족)
            if (stripped[0] == "-" or stripped[0] == "*") and _is_horizontal_bar(stripped):
                above_empty = result_lines and result_lines[-1].strip() == ""
                below_empty = i < len(lines) - 1 and lines[i + 1].strip() == ""

                # 위/아래 모두 빈 줄인 경우, 위의 빈 줄도 함께 제거
                if above_empty and below_empty:
                    result_lines.pop()
                    i += 1
                # 위/아래 중 하나만 빈 줄인 경우, horizontal bar 제거
                elif above_empty or below_empty:
                    i += 1
                # 위/아래 모두 빈 줄이 아닌 경우, horizontal bar를 빈 줄로 대체
                else:
                    result_lines.append("")
                    i += 1
            # horizontal bar가 아닌 경우 그대로 추가
            else:
                result_lines.append(line)
                i += 1

        # 처리된 줄들을 다시 합쳐서 반환
        return "\n".join(result_lines)


def _is_horizontal_bar(line: str) -> bool:
    """주어진 line이 horizontal bar인지 판단합니다.

    Horizontal bar는 `-` 또는 `*`가 3개 이상 반복되며,
    중간에 공백이 포함될 수 있습니다.
    """

    # `-`로 시작하는 경우
    if line[0] == "-":
        # `-`와 공백만 포함되어야 함
        if all(c in "- " for c in line):
            dash_count = line.count("-")
            if dash_count >= 3:
                return True

    # `*`로 시작하는 경우
    elif line[0] == "*":
        # `*`와 공백만 포함되어야 함
        if all(c in "* " for c in line):
            asterisk_count = line.count("*")
            if asterisk_count >= 3:
                return True

    return False
