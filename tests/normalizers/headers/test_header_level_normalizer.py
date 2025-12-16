import re

import pytest

from mdfix.normalizers.headers import HeaderLevelNormalizer


@pytest.mark.parametrize(
    "input_text,expected",
    [
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No headers", "No headers", id="no_headers"),  # 헤더_없음
        pytest.param("# H1\n## H2", "# H1\n## H2", id="min_level_1_no_change_a"),  # 최소레벨1_변경없음_a
        pytest.param("# H1", "# H1", id="min_level_1_no_change_b"),  # 최소레벨1_변경없음_b
        pytest.param("### H3", "## H3", id="h3_alone_to_h2"),  # h3_단독_h2로
        pytest.param("#### H4", "## H4", id="h4_alone_to_h2"),  # h4_단독_h2로
        pytest.param("# H1\n### H3", "# H1\n### H3", id="min_level_1_no_change_mixed"),  # 최소레벨1_변경없음_혼합
        pytest.param("## H2\n#### H4", "## H2\n#### H4", id="min_level_2_no_change"),  # 최소레벨2_변경없음
        pytest.param(
            "### H3\n#### H4\n##### H5", "## H3\n### H4\n#### H5", id="all_levels_normalized"
        ),  # 모든_레벨_정규화됨
    ],
)
def test_normalize_header_levels_cases(input_text, expected):
    result = HeaderLevelNormalizer()(input_text)
    assert result == expected

    # Verify min level is at most 2
    header_pattern = re.compile(r"^(#{1,6})\s+", re.MULTILINE)
    headers = header_pattern.findall(result)
    if headers:
        min_level = min(len(h) for h in headers)
        assert min_level <= 2, f"Min level should be <= 2, got {min_level}"
