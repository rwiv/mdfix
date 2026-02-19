import pytest

from mdfix.headers import HeaderNumberMarkerConverter


# fmt: off
@pytest.mark.parametrize(
    "input_text,expected",
    [
        # 기본 케이스
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No headers here", "No headers here", id="no_headers"),  # 헤더_없음

        # 단일 원형 숫자 변환
        pytest.param("## ② two", "## 2) two", id="circled_two"),  # 원형_2

        # H1 케이스
        pytest.param("# ① one", "# ① one", id="circled_one"),  # 원형_1

        # 높은 숫자
        pytest.param("## ⑩ ten", "## 10) ten", id="circled_ten"),  # 원형_10
        pytest.param("## ⑮ fifteen", "## 15) fifteen", id="circled_fifteen"),  # 원형_15
        pytest.param("### ⑳ twenty", "### 20) twenty", id="circled_twenty"),  # 원형_20

        # 다중 원형 숫자
        pytest.param(
            "## ① first ② second",
            "## 1) first 2) second",
            id="multiple_circled_numbers",
        ),  # 다중_원형_숫자

        # 다중 헤더
        pytest.param(
            "## ① Header One\n### ② Header Two",
            "## 1) Header One\n### 2) Header Two",
            id="multiple_headers",
        ),  # 다중_헤더

        # 이미 일반 숫자인 경우
        pytest.param("## 1 already normal", "## 1 already normal", id="already_normal"),  # 이미_정규화됨

        # 혼합 시나리오
        pytest.param("## ① first\n### Regular header", "## 1) first\n### Regular header", id="mixed_circled_and_normal"),  # 혼합
    ],
)
# fmt: on
def test_header_number_marker_converter(input_text, expected):
    assert HeaderNumberMarkerConverter()(input_text) == expected


# fmt: off
@pytest.mark.parametrize(
    "input_text,expected,delimiter",
    [
        # 커스텀 delimiter 테스트
        pytest.param("## ① one", "## 1. one", ".", id="dot_delimiter"),  # 점_구분자
        pytest.param("## ② two", "## 2: two", ":", id="colon_delimiter"),  # 콜론_구분자
    ],
)
# fmt: on
def test_header_number_marker_converter_with_delimiter(input_text, expected, delimiter):
    assert HeaderNumberMarkerConverter(delimiter=delimiter)(input_text) == expected
