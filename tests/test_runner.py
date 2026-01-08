import sys
import os
from unittest.mock import patch

from mdfix.runner import get_argv_paths, normalize_md


class TestGetPaths:
    def test_no_arguments(self):
        """인자가 없으면 빈 리스트 반환"""
        with patch.object(sys, "argv", ["script.py"]):
            assert get_argv_paths() == []

    def test_single_path(self):
        """단일 경로 인자"""
        with patch.object(sys, "argv", ["script.py", "/path/to/file.md"]):
            assert get_argv_paths() == ["/path/to/file.md"]

    def test_multiple_paths(self):
        """다중 경로 인자"""
        with patch.object(sys, "argv", ["script.py", "file1.md", "file2.md", "file3.md"]):
            assert get_argv_paths() == ["file1.md", "file2.md", "file3.md"]

    def test_paths_with_spaces(self):
        """공백이 포함된 경로"""
        with patch.object(sys, "argv", ["script.py", "/path/with spaces/file.md"]):
            assert get_argv_paths() == ["/path/with spaces/file.md"]

    def test_absolute_paths(self):
        """절대 경로"""
        with patch.object(sys, "argv", ["script.py", "C:\\Users\\test\\file.md"]):
            assert get_argv_paths() == ["C:\\Users\\test\\file.md"]


class TestConvMd:
    def test_empty_paths_list(self, tmp_path):
        """빈 경로 리스트는 아무것도 하지 않음"""
        normalize_md([])
        # No files should be created
        assert len(list(tmp_path.glob("*"))) == 0

    def test_single_file_conversion(self, tmp_path):
        """단일 파일 변환"""
        input_file = tmp_path / "test.md"
        input_file.write_text("# Header\nContent", encoding="utf-8")

        normalize_md([str(input_file)])

        output_file = tmp_path / "test_out.md"
        assert output_file.exists()
        content = output_file.read_text(encoding="utf-8")
        assert "# Header" in content
        assert "Content" in content

    def test_multiple_files(self, tmp_path):
        """다중 파일 처리"""
        file1 = tmp_path / "file1.md"
        file2 = tmp_path / "file2.md"
        file1.write_text("# File 1", encoding="utf-8")
        file2.write_text("# File 2", encoding="utf-8")

        normalize_md([str(file1), str(file2)])

        assert (tmp_path / "file1_out.md").exists()
        assert (tmp_path / "file2_out.md").exists()

    def test_output_file_naming(self, tmp_path):
        """출력 파일에 _out 접미사 추가"""
        input_file = tmp_path / "document.md"
        input_file.write_text("Content", encoding="utf-8")

        normalize_md([str(input_file)])

        output_file = tmp_path / "document_out.md"
        assert output_file.exists()

    def test_utf8_encoding(self, tmp_path):
        """한글 문자로 UTF-8 인코딩 보존"""
        input_file = tmp_path / "korean.md"
        korean_text = "# 한글 헤더\n테스트 내용입니다."
        input_file.write_text(korean_text, encoding="utf-8")

        normalize_md([str(input_file)])

        output_file = tmp_path / "korean_out.md"
        content = output_file.read_text(encoding="utf-8")
        assert "한글 헤더" in content
        assert "테스트 내용입니다" in content

    def test_full_transformation_pipeline(self, tmp_path):
        """모든 패턴으로 완전한 변환"""
        input_file = tmp_path / "test.md"
        input_content = """
## Header
*   List item
1)  Numbered
  - hello
# Deep header 1
### Deep header 3
\\[ x^2 + y^2 = z^2 \\]
Inline math \\(a + b\\) here
"""

        input_file.write_text(input_content, encoding="utf-8")
        normalize_md(paths=[str(input_file)], mode="default")

        output_file = tmp_path / "test_out.md"
        assert output_file.exists()

        output_content = output_file.read_text(encoding="utf-8")
        expected_output_content = """
## Header

- List item
1. Numbered
    - hello
# Deep header 1
### Deep header 3

$$x^2 + y^2 = z^2$$
Inline math $a + b$ here
"""
        # Verify all normalizations
        assert output_content == expected_output_content

    def test_nested_directory(self, tmp_path):
        """중첩 디렉토리의 파일 처리"""
        nested_dir = tmp_path / "subdir" / "nested"
        nested_dir.mkdir(parents=True)
        input_file = nested_dir / "file.md"
        input_file.write_text("# Content", encoding="utf-8")

        normalize_md([str(input_file)])

        output_file = nested_dir / "file_out.md"
        assert output_file.exists()

    def test_file_without_extension(self, tmp_path):
        """확장자 없는 파일 처리"""
        input_file = tmp_path / "noext"
        input_file.write_text("# Content", encoding="utf-8")

        normalize_md([str(input_file)])

        output_file = tmp_path / "noext_out"
        assert output_file.exists()

    def test_file_with_multiple_dots(self, tmp_path):
        """여러 점이 포함된 파일명 처리"""
        input_file = tmp_path / "file.name.with.dots.md"
        input_file.write_text("# Content", encoding="utf-8")

        normalize_md([str(input_file)])

        output_file = tmp_path / "file.name.with.dots_out.md"
        assert output_file.exists()

    def test_relative_path(self, tmp_path):
        """상대 경로 처리"""
        input_file = tmp_path / "relative.md"
        input_file.write_text("# Content", encoding="utf-8")

        # Use relative path
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            normalize_md(["relative.md"])
            assert (tmp_path / "relative_out.md").exists()
        finally:
            os.chdir(original_cwd)
