import pytest

from mdfix.spaces import PaddingLineRemover


@pytest.mark.parametrize(
    "input_text,expected",
    # fmt: off
    [
        # 기본 케이스
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("hello world", "hello world", id="no_padding_lines"),  # 공백_줄_없음
        pytest.param("hello\nworld", "hello\nworld", id="normal_text_with_newline"),  # 일반_텍스트_개행

        # 1-3개 공백 (제거되지 않음)
        pytest.param(" \ntext", " \ntext", id="single_space_line"),  # 1개_공백_줄
        pytest.param("  \ntext", "  \ntext", id="two_spaces_line"),  # 2개_공백_줄
        pytest.param("   \ntext", "   \ntext", id="three_spaces_line"),  # 3개_공백_줄

        # 단일 padding line (4개 이상 공백)
        pytest.param("    \ntext", "text", id="four_spaces_line"),  # 정확히_4개_공백_줄
        pytest.param("     \ntext", "text", id="five_spaces_line"),  # 5개_공백_줄
        pytest.param("          \ntext", "text", id="ten_spaces_line"),  # 많은_공백_(10개)

        # 다중 padding line (연속)
        pytest.param("    \n    \ntext", "text", id="two_padding_lines"),  # 연속된_2개_padding_줄
        pytest.param("    \n    \n    \ntext", "text", id="three_padding_lines"),  # 연속된_3개_padding_줄

        # 여러 위치의 padding line
        pytest.param("text\n    \nmore", "text\nmore", id="padding_in_middle"),  # 중간의_padding_줄
        pytest.param("    \ntext\n    \nmore", "text\nmore", id="padding_at_start_and_middle"),  # 시작과_중간의_padding

        # 시작 부분의 padding line
        pytest.param("    \ntext", "text", id="padding_at_start"),  # 시작_부분_padding
        pytest.param("    \n    \ntext", "text", id="multiple_padding_at_start"),  # 시작의_다중_padding

        # 혼합 케이스 (빈 줄 보존)
        pytest.param("text\n\nmore", "text\n\nmore", id="blank_line_preserved"),  # 빈_줄_보존
        pytest.param("text\n    \n\nmore", "text\n\nmore", id="padding_and_blank_lines"),  # padding과_빈줄_혼합

        # 코드 블록 케이스 (feat_plan.md)
        pytest.param(
            "```\n    \ncode\n```",
            "```\n    \ncode\n```",
            id="padding_in_code_block_preserved"
        ),  # 코드_블록_내부_padding_보존
        pytest.param(
            "```\ncode\n```\n    \ntext",
            "```\ncode\n```\ntext",
            id="padding_outside_code_block_removed"
        ),  # 코드_블록_외부_padding_제거
        pytest.param(
            "    \n```\n    \ncode\n```\n    \n",
            "```\n    \ncode\n```\n",
            id="mixed_padding_and_code_block"
        ),  # 혼합_케이스

        # 엣지 케이스
        pytest.param("    text", "    text", id="spaces_with_text_no_newline"),  # 공백과_텍스트_(개행_없음)
        pytest.param("\ttext", "\ttext", id="tab_character"),  # 탭_문자
        pytest.param("  \t  \ntext", "  \t  \ntext", id="mixed_spaces_and_tabs"),  # 공백과_탭_혼합
    ],
    # fmt: on
)
def test_padding_line_remover(input_text, expected):
    assert PaddingLineRemover()(input_text) == expected
