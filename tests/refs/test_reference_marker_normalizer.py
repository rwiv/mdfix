import pytest

from mdfix.refs import ReferenceMarkerNormalizer


# fmt: off
@pytest.mark.parametrize(
    "input_text,expected",
    [
        # 기본 케이스
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No brackets here", "No brackets here", id="no_brackets"),  # 괄호_없음

        # 숫자 괄호 변환
        pytest.param("[1] Start", "[^1] Start", id="bracket_at_line_start"),  # 줄_시작_괄호
        pytest.param("hello. [1]", "hello. [^1]", id="bracket_at_end"),  # 끝_괄호
        pytest.param("a [1] b", "a [^1] b", id="bracket_in_middle"),  # 중간_괄호
        pytest.param("a [1] b  [2]", "a [^1] b  [^2]", id="multiple_brackets"),  # 다중_괄호

        # 다양한 번호
        pytest.param("Multi [123]", "Multi [^123]", id="multi_digit"),  # 여러_자리수
        pytest.param(" [1] [2] [3]", " [^1] [^2] [^3]", id="consecutive_brackets"),  # 연속된_여러_괄호

        # 공백 처리
        pytest.param("hello[1] .", "hello[^1] .", id="no_space_before_bracket"),  # 공백_없이_대괄호
        pytest.param("hello [1].", "hello [^1].", id="bracket_before_punct"),  # 괄호_구두점_앞
        pytest.param("hello [1] .", "hello [^1] .", id="bracket_with_space"),  # 괄호_양옆_공백

        # 비숫자 괄호는 변환 안 함
        pytest.param("[abc] not changed", "[abc] not changed", id="not_numeric"),  # 숫자_아님
        pytest.param("Mixed [1] [abc]", "Mixed [^1] [abc]", id="mixed_brackets"),  # 혼합_괄호

        # 참고문헌 정의 형식 변환 - 단일 참조
        pytest.param(
            "This is [^1] text\n[^1](https://example.com)",
            "This is [^1] text\n[^1]: https://example.com",
            id="single_reference_definition",
        ),  # 단일_참고문헌_정의

        # 참고문헌 정의 형식 변환 - 다중 참조
        pytest.param(
            "See [^1] and [^2]\n[^1](https://example1.com)\n[^2](https://example2.com)",
            "See [^1] and [^2]\n[^1]: https://example1.com\n[^2]: https://example2.com",
            id="multiple_reference_definitions",
        ),  # 다중_참고문헌_정의

        # 미사용 참고문헌 삭제
        pytest.param(
            "This is [^1] text\n[^1](https://example.com)\n[^2](https://unused.com)",
            "This is [^1] text\n[^1]: https://example.com",
            id="unused_reference_deleted",
        ),  # 미사용_참고문헌_삭제

        # 숫자 변환 + 정의 형식 변환
        pytest.param(
            "See [1]\n[^1](https://example.com)",
            "See [^1]\n[^1]: https://example.com",
            id="numeric_to_footnote_to_definition",
        ),  # 숫자_변환_정의_형식

        # 정의 형식이 먼저 나오는 경우
        pytest.param(
            "[^1](https://example.com)\nSee [^1]",
            "[^1]: https://example.com\nSee [^1]",
            id="definition_before_reference",
        ),  # 정의_참조_이전

        # 여러 줄의 참고문헌
        pytest.param(
            "Text [1]\n[^1](url1)\nMore text [2]\n[^2](url2)",
            "Text [^1]\n[^1]: url1\nMore text [^2]\n[^2]: url2",
            id="multiple_lines_references",
        ),  # 여러_줄_참고문헌

        # URL에 공백 및 특수문자 포함
        pytest.param(
            "See [^1]\n[^1](https://example.com/path?query=value&other=123)",
            "See [^1]\n[^1]: https://example.com/path?query=value&other=123",
            id="complex_url",
        ),  # 복잡한_URL

        # 빈 정의 (URL이 없는 경우)
        pytest.param(
            "See [^1]\n[^1]()",
            "See [^1]\n[^1]: ",
            id="empty_url_definition",
        ),  # 빈_URL_정의

        # 세 자리 이상 번호
        pytest.param(
            "See [^123]\n[^123](https://example.com)",
            "See [^123]\n[^123]: https://example.com",
            id="multi_digit_reference",
        ),  # 여러_자리_참고문헌
    ],
)
# fmt: on
def test_reference_marker_normalizer(input_text, expected):
    assert ReferenceMarkerNormalizer()(input_text) == expected
