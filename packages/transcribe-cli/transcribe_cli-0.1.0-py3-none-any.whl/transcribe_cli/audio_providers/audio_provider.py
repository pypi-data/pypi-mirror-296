from abc import ABC, abstractmethod
from typing import Optional

class AudioProvider(ABC):
    @abstractmethod
    def download_audio(self) -> Optional[str]:
        pass
