import pytest

from mdfix.normalizers.headers import HeaderEmphasisRemover


@pytest.mark.parametrize(
    "input_text,expected",
    # fmt: off
    [
        # 기본 케이스
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No headers here", "No headers here", id="no_headers"),  # 헤더_없음

        # 단일 헤더 강조 표시 제거
        pytest.param("# **bold**", "# bold", id="h1_bold"),  # h1_bold
        pytest.param("## *italic*", "## italic", id="h2_italic"),  # h2_italic
        pytest.param("### _emphasis_", "### emphasis", id="h3_emphasis"),  # h3_emphasis

        # 혼합 강조 표시
        pytest.param("# **bold** *italic*", "# bold italic", id="mixed_emphasis"),  # 혼합_강조
        pytest.param("## ***bold_italic***", "## bold_italic", id="triple_emphasis"),  # triple_emphasis

        # 다중 헤더
        pytest.param(
            "# **Header 1**\n## *Header 2*",
            "# Header 1\n## Header 2",
            id="multiple_headers",
        ),  # 다중_헤더

        # 헤더 내용 유지
        pytest.param("# Normal text", "# Normal text", id="no_emphasis_text"),  # 강조_없는_텍스트
        pytest.param("## Text with **partial** bold", "## Text with partial bold", id="partial_emphasis"),  # 부분_강조

        # 엣지 케이스
        pytest.param("# _**mixed**_", "# mixed", id="mixed_emphasis_marks"),  # 혼합_강조_마크
        pytest.param("#### **___all___**", "#### all", id="complex_nested_emphasis"),  # 복잡한_중첩_강조

        # 일반 텍스트는 변경 없음
        pytest.param("Text with **bold** here", "Text with **bold** here", id="non_header_text"),  # 헤더_아님_텍스트
    ],
    # fmt: on
)
def test_header_emphasis_remover(input_text, expected):
    assert HeaderEmphasisRemover()(input_text) == expected
