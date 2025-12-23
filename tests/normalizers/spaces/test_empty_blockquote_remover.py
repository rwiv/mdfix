import pytest

from mdfix.normalizers.spaces import EmptyBlockquoteRemover


@pytest.mark.parametrize(
    "input_text,expected",
    # fmt: off
    [
        # 기본 케이스
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("hello world", "hello world", id="no_blockquote"),  # blockquote_없음
        pytest.param("> content\n", "> content\n", id="non_empty_blockquote"),  # 내용이_있는_blockquote

        # 단일 빈 blockquote (제거해야 함)
        pytest.param(">\n", "", id="empty_blockquote_only"),  # blockquote만_있는_경우
        pytest.param("> \n", "", id="empty_blockquote_with_space"),  # blockquote_뒤에_공백
        pytest.param(">  \n", "", id="empty_blockquote_multiple_spaces"),  # blockquote_뒤에_여러_공백
        pytest.param(">   \n", "", id="empty_blockquote_three_spaces"),  # blockquote_뒤에_3개_공백

        # 빈 blockquote가 포함된 경우
        pytest.param("hello\n>\nworld", "hello\nworld", id="empty_blockquote_between_text"),  # 텍스트_사이의_빈_blockquote
        pytest.param("> content\n>\nmore content", "> content\nmore content", id="empty_blockquote_between_content"),  # 내용_blockquote_사이의_빈_blockquote
        pytest.param("text\n> \nmore", "text\nmore", id="empty_blockquote_with_space_between"),  # 공백있는_빈_blockquote

        # 다중 빈 blockquote
        pytest.param(">\n>\n", "", id="multiple_empty_blockquotes"),  # 연속된_빈_blockquote
        pytest.param(">\n> \n>\n", "", id="mixed_empty_blockquotes"),  # 공백_여부가_다른_빈_blockquote
        pytest.param("text\n>\n>\nmore", "text\nmore", id="consecutive_empty_blockquotes"),  # 텍스트_사이의_연속_빈_blockquote

        # 엣지 케이스
        pytest.param(">\n", "", id="start_empty_blockquote"),  # 시작_부분의_빈_blockquote
        pytest.param("hello\n>\n", "hello\n", id="end_empty_blockquote"),  # 끝_부분의_빈_blockquote
        pytest.param("> content\n>\n> more\n", "> content\n> more\n", id="mixed_empty_and_content"),  # 빈_blockquote와_내용_blockquote_혼합
        pytest.param("> \n> content\n", "> content\n", id="empty_before_content"),  # 빈_blockquote_다음_내용_blockquote
        pytest.param("> content\n> \n", "> content\n", id="content_before_empty"),  # 내용_blockquote_다음_빈_blockquote

        # blockquote 기호 다음 다른 문자 (제거되지 않아야 함)
        pytest.param(">a\n", ">a\n", id="blockquote_with_text"),  # blockquote_뒤에_텍스트
        pytest.param("> text\n", "> text\n", id="blockquote_with_space_and_text"),  # blockquote_공백_텍스트
        pytest.param(">\t\n", ">\t\n", id="blockquote_with_tab"),  # blockquote_뒤에_탭
    ],
    # fmt: on
)
def test_empty_blockquote_remover(input_text: str, expected: str) -> None:
    assert EmptyBlockquoteRemover()(input_text) == expected
