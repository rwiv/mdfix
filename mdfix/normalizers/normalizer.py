from abc import ABC, abstractmethod


class Normalizer(ABC):
    """마크다운 콘텐츠를 변환하는 Normalizer의 추상 기본 클래스"""

    @abstractmethod
    def normalize(self, text: str) -> str:
        """
        마크다운 콘텐츠를 변환합니다.

        Args:
            text: 변환할 마크다운 콘텐츠

        Returns:
            변환된 마크다운 콘텐츠
        """
        pass

    def __call__(self, content: str) -> str:
        """Normalizer를 호출 가능하게 만듭니다."""
        return self.normalize(content)
