import re

import pytest

from mdfix.headers import HeaderLevelNormalizer


@pytest.mark.parametrize(
    "input_text,expected",
    # fmt: off
    [
        # 기본 케이스
        pytest.param("", "", id="empty_string"),  # 빈_문자열
        pytest.param("No headers", "No headers", id="no_headers"),  # 헤더_없음

        # 최소 레벨이 H2 인 경우 (변경 없음)
        pytest.param("## H2\n#### H4", "## H2\n#### H4", id="h2_h4_no_change"),  # h2_h4_변경없음

        # 최소 레벨이 H1 인 경우 (정규화 필요)
        pytest.param("# H1", "# H1", id="h1_alone"),  # h1_단독
        pytest.param("# H1\n## H2", "# H1\n## H2", id="h1_h2_no_change"),  # h1_h2_변경없음
        pytest.param("# H1\n### H3", "# H1\n## H3", id="h1_h3_change"),  # h1_h3_변경없음

        # 최소 레벨이 H2 보다 큰 경우 (정규화 필요)
        pytest.param("### H3", "## H3", id="h3_to_h2"),  # h3_h2로_변환
        pytest.param("#### H4", "## H4", id="h4_to_h2"),  # h4_h2로_변환
        pytest.param("##### H5", "## H5", id="h5_to_h2"),  # h5_h2로_변환
        pytest.param("###### H6", "## H6", id="h6_to_h2"),  # h6_h2로_변환

        # 다중 헤더 정규화
        pytest.param(
            "### H3\n#### H4\n##### H5",
            "## H3\n### H4\n#### H5",
            id="all_levels_normalized",
        ),  # 모든_레벨_정규화
        pytest.param(
            "### Header A\n#### Header B",
            "## Header A\n### Header B",
            id="multiple_consecutive",
        ),  # 연속_다중_헤더
        pytest.param(
            "### H3\n\nSome content\n\n#### H4",
            "## H3\n\nSome content\n\n### H4",
            id="headers_with_content",
        ),  # 내용이_있는_헤더

        # 혼합 시나리오
        pytest.param(
            "# H1\n## H3\n### H4",
            "# H1\n## H3\n### H4",
            id="mixed_with_h1",
        ),  # h1_포함_혼합
        pytest.param(
            "## H2\n### H3\n##### H5",
            "## H2\n### H3\n##### H5",
            id="preserve_relative_levels",
        ),  # 상대적_레벨_유지
    ],
    # fmt: on
)
def test_header_level_normalizer(input_text, expected):
    result = HeaderLevelNormalizer()(input_text)
    assert result == expected

    # Verify min level is at most 2
    header_pattern = re.compile(r"^(#{1,6}) +", re.MULTILINE)
    headers = header_pattern.findall(result)
    if headers:
        min_level = min(len(h) for h in headers)
        assert min_level <= 2, f"Min level should be <= 2, got {min_level}"
