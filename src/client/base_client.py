from abc import ABC, abstractmethod
from typing import Optional

class BaseClient(ABC):
    """TTS 客户端基类"""
    @abstractmethod
    async def connect(self) -> bool:
        """建立连接"""
        pass
    
    @abstractmethod
    async def disconnect(self) -> None:
        """断开连接"""
        pass
    
    @abstractmethod
    async def text_to_speech(self, text: str, voice: str, output_file: str, **kwargs) -> bool:
        """文本转语音"""
        pass