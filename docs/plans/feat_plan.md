# Padding Line Remover 개선 계획

## 목표
Markdown 코드 블록(`code block`) 내부에 위치한 padding line(4개 이상의 공백으로 구성된 줄)은 제거 대상에서 제외하도록 `PaddingLineRemover`를 수정합니다.

## 문제점
현재 구현은 문맥을 고려하지 않고 4개 이상의 공백으로 시작하는 모든 줄을 제거합니다.
```python
re.sub(r"^ {4,}\n", "", text, flags=re.MULTILINE)
```
이로 인해 코드 블록 내부의 의도된 들여쓰기나 공백 라인이 잘못 제거될 수 있습니다.

## 제안 솔루션
정규표현식의 분기(alternation) 기능을 사용하여 "코드 블록" 또는 "제거 대상 padding line"을 동시에 매칭합니다. `re.sub`의 콜백 함수를 활용하여 매칭된 그룹에 따라 보존할지 제거할지 결정합니다.

### 정규표현식 전략
두 가지 주요 그룹을 포함하는 정규식을 구성합니다:
1. **코드 블록 그룹**: Fenced code block (``` 또는 ~~~ 로 시작)을 매칭합니다.
2. **Padding Line 그룹**: 제거하고자 하는 padding line을 매칭합니다.

**패턴 예시:**
```regex
(?ms)(^(`{3,}|~{3,}).*?^\2)|(^ {4,}\n)
```
*   `(?ms)`: MULTILINE ( `^`가 줄의 시작과 매칭) 및 DOTALL ( `.`이 개행 문자와 매칭) 모드를 활성화합니다.
*   **그룹 1**: 전체 코드 블록.
    *   `^(`{3,}|~{3,})`: 시작 펜스 (Backtick 또는 Tilde 3개 이상). (내부 그룹 2로 캡처하여 닫는 펜스에서 참조)
    *   `.*?`: 내부 콘텐츠 (non-greedy).
    *   `^\2`: 시작 펜스와 동일한 닫는 펜스.
*   **그룹 3**: 타겟 Padding line (`^ {4,}\n`).

### 로직
`re.sub`를 사용하여 텍스트를 순회합니다:
- **그룹 1 (코드 블록)**이 매칭된 경우: 매칭된 텍스트를 그대로 반환합니다 (보존).
- **그룹 3 (Padding Line)**이 매칭된 경우: 빈 문자열을 반환합니다 (제거).

### 구현 단계
1.  `mdfix/normalizers/spaces/padding_line_remover.py`의 `normalize` 메서드를 수정합니다.
2.  위의 전략을 적용한 결합된 정규표현식을 정의합니다.
3.  `re.sub(pattern, callback, text)`를 호출합니다.
    - `callback` 함수는 `match.group(1)`(코드 블록)이 존재하는지 확인합니다.
    - 존재하면 `match.group(1)`을 반환합니다.
    - 존재하지 않으면(즉, padding line 매칭이면) 빈 문자열 `""`을 반환합니다.

## 검증
- `tests/normalizers/spaces/test_padding_line_remover.py`에 테스트 케이스를 추가합니다.
    - 코드 블록 내부에 4개 이상의 공백 줄이 있는 경우 제거되지 않는지 확인.
    - 코드 블록 외부의 4개 이상의 공백 줄은 여전히 정상적으로 제거되는지 확인.
