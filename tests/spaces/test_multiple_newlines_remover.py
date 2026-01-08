import pytest

from mdfix.spaces import MultipleNewlinesRemover


@pytest.mark.parametrize(
    "input_text,expected",
    # fmt: off
    [
        # 기본 케이스
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("hello world", "hello world", id="no_newlines"),  # 개행_없는_텍스트

        # 단일 개행 (변환 불필요)
        pytest.param("hello\nworld", "hello\nworld", id="single_newline"),  # 1개_개행
        pytest.param("hello\n\nworld", "hello\n\nworld", id="double_newline"),  # 2개_개행

        # 3개 이상 개행 (변환 필요)
        pytest.param("hello\n\n\nworld", "hello\n\nworld", id="triple_newline"),  # 정확히_3개_개행
        pytest.param("hello\n\n\n\nworld", "hello\n\nworld", id="quadruple_newline"),  # 4개_개행
        pytest.param("hello\n\n\n\n\nworld", "hello\n\nworld", id="quintuple_newline"),  # 5개_개행
        pytest.param("text\n\n\n\n\n\n\n\n\n\nmore", "text\n\nmore", id="many_newlines"),  # 많은_개행_(10개)

        # 다중 위치에서의 개행
        pytest.param("a\n\n\nb\n\n\n\nc", "a\n\nb\n\nc", id="multiple_groups"),  # 여러_개의_3개_이상_개행_그룹
        pytest.param("text\n\nmore\n\n\nstuff", "text\n\nmore\n\nstuff", id="mixed_newlines"),  # 혼합_(2개_이후_3개_이상)

        # 엣지 케이스
        pytest.param("\n\n\nhello", "\n\nhello", id="start_triple_newline"),  # 시작_부분의_3개_개행
        pytest.param("hello\n\n\n", "hello\n\n", id="end_triple_newline"),  # 끝_부분의_3개_개행
        pytest.param("\n\n\n\n", "\n\n", id="only_newlines"),  # 오직_개행만
        pytest.param("hello \n\n\n world", "hello \n\n world", id="newline_with_spaces"),  # 개행과_공백_혼합
        pytest.param("hello\t\n\n\nworld", "hello\t\n\nworld", id="tab_with_newlines"),  # 탭과_개행_혼합
    ],
    # fmt: on
)
def test_multiple_newlines_remover(input_text, expected):
    assert MultipleNewlinesRemover()(input_text) == expected
