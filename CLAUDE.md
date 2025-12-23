## General Coding Standards

### Core Principles

- 모든 주석(Comments)과 문서(Docs)는 한글로 작성한다.
- 별도의 명시적인 요청이 없다면 Test Plan과 Test Code는 작성하지 않는다. (Production Code 우선)
- 모든 함수와 메서드 시그니처에 Python Type Hint를 명시한다.

### Docstring-based Implementation

- **Before Implementation**: 구현해야할 클래스/함수에 Docstring이 존재한다면 이를 기반으로 구현한다.
- **After Implementation**: 코드의 Docstring은 코드의 명세가 된다. 작성된 코드의 내용과 가독성을 고려하여 Docstring을 적절하게 수정한다.

### Module Specification & Context

- **Spec Index Path**: `docs/_build/markdown/mdfix/modules.md`
- 모듈 명세에는 클래스/함수의 시그니처와 설명이 포함된다.
- **Context Loading**: 모듈 명세만으로 정보가 충분하다면 불필요하게 원본 코드 파일을 읽지 않아 토큰을 절약한다. 단, 모호한 경우에는 원본을 확인한다.

## Architecture & Patterns

### `Normalizer` Implementation

[Normalizer](mdfix/normalizers/normalizer.py) 구현 시 다음 규칙을 따른다:
- **Reference Path**: `mdfix/normalizers/headers/header_emphasis_remover.py`의 구조와 패턴을 참고하여 일관성을 유지한다.
- **Implementation Path**: 구현체는 `mdfix/normalizers/` 내 적절한 위치에 배치한다.
- **Testing Path**: 관련 테스트는 `tests/normalizers/` 내부에 작성한다.

## Testing Workflow

### 1. Test Plan (Optional)

- **File Path**: `specs/TESTPLAN.md`
- **Overwrite Rule**: 새로운 기능을 테스트할 때는 기존 내용을 무시하고 덮어쓴다(Overwrite). 기존 기능을 수정할 때는 부분 업데이트한다.
- **Format**
    - 한글로 작성 한다.
    - Table 대신 Header/List 구조를 사용한다.

**Required Contents**:
1. **Target Paths**: 구현할 테스트 파일 경로
2. **Test Suite & Cases**:
    - 각 Test Case는 Edge Case를 반드시 포함해야 한다.
    - 테스트 대상 클래스/함수 명시.
3. **Dependencies**: 의존성 목록 및 Test Double(Mock/Stub) 사용 여부.
4. **Tools**: 사용할 라이브러리/API (예: `@pytest.mark.parametrize`)와 선정 이유.

### 2. Test Code Implementation

- **Description**: 각 테스트 케이스마다 의도를 간단히 설명하는 한글 주석을 포함한다.
- **Reference**: `tests/normalizers/spaces/test_multiple_newlines_remover.py` 스타일을 참고한다.
- **Execution**: 작성된 테스트 코드는 AI가 직접 실행하지 않는다 (유저가 실행).
