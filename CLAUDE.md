## Project Overview

- 본 프로젝트는 RAG(Retrieval-Augmented Generation) 시스템의 검색 정확도와 답변 품질을 극대화하기 위해, 문서를 단순한 길이 기반이 아닌 **의미론적(Semantic) 및 구조적(Structural) 계층 트리**로 분해하는 전처리 파이프라인이다.
- 기존의 Flat Chunking 방식이 갖는 맥락 소실 문제를 해결하기 위해, 상위 노드의 맥락(Context)을 하위 노드로 전파(Injection)하며 재귀적으로 문서를 분할한다.

## Document References

작업 수행 전, 필요한 문서를 **반드시** 읽고 나서 작업을 수행하라.

- `docs/plan/feat_plan.md`: feature plan spec
- `docs/plan/test_plan.md`: test plan spec
- `docs/plan/debug_plan.md`: debugging plan spec
- `docs/plan/request.md`: 작업 실행을 위한 추가적인 요청 문서

## **CRITICAL INSTRUCTION: No Auto-Progression**

**절대로 다음 작업을 멋대로 실행하지 마시오.**

- feature plan 작성이 끝나도 code 구현을 시도하지 않는다.
- feature code 작성이 끝나도 code 구현/실행을 시도하지 않는다.
- test plan 작성이 끝나도 test code 구현을 시도하지 않는다.
- test code 작성이 끝나도 test code를 실행하지 않는다.
- 절대 멋대로 git add, git commit을 수행하지 마라.

## Planing Rules

- 모든 plan 명세는 **한글**로 작성한다.
- 수정이 힘들어지므로 markdown table 사용을 가급적 자제하라.
- 기존 plan 파일에 내용이 남아있는 경우
  - 현재 작성하는 내용과 완전히 다른 내용일 경우: 사용자가 미처 지우지 못한 내용이므로 overwrite한다.
  - 현재 작성하는 내용과 같은 내용일 경우: 기존 plan 파일 내용을 기반으로 디테일을 수정한다.

## Execution Command

- python 커맨드를 실행할 땐 uv를 사용한다. (e.g. `uv run pyright`)

## Implementation Guidelines

### General Coding Standards

#### Core Principles

- 모든 주석(Comments)과 문서(Docs)는 한글로 작성한다.
- 별도의 명시적인 요청이 없다면 Test Plan과 Test Code는 작성하지 않는다. (Production Code 우선)
- 모든 함수와 메서드 시그니처에 Python Type Hint를 명시한다.

#### Docstring-based Implementation

- **Before Implementation**: 구현해야할 클래스/함수에 Docstring이 존재한다면 이를 기반으로 구현한다.
- **After Implementation**: 코드의 Docstring은 코드의 명세가 된다. 작성된 코드의 내용과 가독성을 고려하여 Docstring을 적절하게 수정한다.

### `Normalizer` Implementation

[Normalizer](mdfix/normalizer.py) 구현 시 다음 규칙을 따른다:
- **Reference Path**: `mdfix/normalizers/headers/header_emphasis_remover.py`의 구조와 패턴을 참고하여 일관성을 유지한다.
- **Implementation Path**: 구현체는 `mdfix/normalizers/` 내 적절한 위치에 배치한다.
- **Testing Path**: 관련 테스트는 `tests/normalizers/` 내부에 작성한다.

## Testing Guidelines

### Test Double Implementation Guilde

#### Fake Test Double

- fake repository는 dict, list, set 등 python 자료구조를 활용해 구현한다.

#### Dummy Test Double

- dummy 데이터를 생성하는 코드가 중복된다면 util/helper 함수로 따로 빼서 관리한다.
- dummy 데이터의 content는 명시적으로 확인해야하는 데이터가 아니라면 Faker를 사용해서 채운다.

### Writing Test Plan

- `docs/plans/test_plan.md`에 작성하라.
- 반드시 **한글**로 작성하라.
- 수정이 힘들어지므로 markdown table 사용을 가급적 자제하라.
- **test plan 작성이 끝나도 test code 구현을 시도하지 않는다.**

#### Required Contents

1. **Target Paths**: 구현할 테스트 파일 경로
2. **Test Suite**:
   - 후술할 Test Suite Structure 중 하나를 선택해서 작성.
   - 테스트 대상 클래스/함수 명시.
3. **Dependencies**: 의존성 목록 및 Test Double(Mock/Stub) 사용 여부.
4. **Tools**: 사용할 라이브러리/API (예: `@pytest.mark.parametrize`)와 선정 이유.
5. **Existing Tests** (Optional): 기존 존재하는 테스트 코드의 처우 (수정할건지, 놔둘건지, 삭제할건지)
  - 테스트 파일이 존재하지 않는다면 작성할 필요 없다.

#### Test Suite Structure

- 후술할 Test Suite Structure를 기반으로 test cases를 구조적으로 작성한다.
- 비즈니스 로직은 `Business-based Structure`를, 그 이외 로직은 `Logic-based Structure`를 사용한다.

**Business-based Structure**:

1. Standard Scenarios: 가장 표준적인 성공 상황들 (예: 쿠폰 없이 결제, 쿠폰 쓰고 결제)
2. Alternate Scenarios: 성공은 하지만 경로가 다른 경우 (예: 포인트 전액 결제, 부분 취소 후 재결제)
3. Failure Scenarios: 비즈니스 규칙 위반으로 실패하는 경우 (예: 잔액 부족, 유효기간 만료, 중복 결제)
4. Complex Scenarios (Optional): 복합 시나리오. (예: DB 연결이 끊긴 상태에서 요청, 중복 요청, 의존성 객체의 데이터가 꼬여있을 때)

**Logic-based Structure**:

1. Core Cases: 가장 표준적인 케이스들. 분기에 따라 2개 이상이 될 수도 있다. Happy Path를 포함한다.
2. Edge Cases: boundary case, 예외적 상황, 극단적 상황, 특수 분기 케이스 등
3. Error Cases: error & null을 발생시키는 케이스
4. Complex Scenarios (Optional): 복합 시나리오. (예: DB 연결이 끊긴 상태에서 요청, 중복 요청, 의존성 객체의 데이터가 꼬여있을 때)

### Test Code Implementation

`docs/plans/test_plan.md`를 기반으로 테스트 코드를 작성한다.

- 각 테스트 케이스마다 의도를 간단히 설명하는 한글 주석을 포함한다.
- **test code 작성이 끝나도 test code를 실행하지 않는다.**
- 테스트 코드 파일을 생성하기 위해 directory를 생성해야한다면 반드시 비어있는 `__init__.py`를 같이 생성한다.

#### Pytest Rules

다음처럼 구조적인 테스트 코드 블럭에는 `fmt: off`, `fmt: on`를 붙여라.

```python
@pytest.mark.parametrize(
    "text, expected",
    # fmt: off
    [
        ## 1. Basic Punctuation
        ("Hello world.", ["Hello world."]),
        ## 2. Multiple Sentences
        ("Hello world. This is a test.", ["Hello world.", "This is a test."]),
        # ...
    ],
    # fmt: on
)
```
