from src.client.base_client import BaseClient
import edge_tts
import asyncio
from typing import Dict, Any

class EdgeTTSClient(BaseClient):
    def __init__(self, max_retries: int = 3, retry_delay: int = 1):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
    async def connect(self) -> bool:
        return True  # Edge TTS 不需要持久连接
        
    async def disconnect(self) -> None:
        pass  # Edge TTS 不需要断开连接
        
    async def text_to_speech(self, text: str, config: Dict[str, Any], output_file: str) -> bool:
        voice = config.get('voice', 'zh-CN-XiaoxiaoNeural')
        for attempt in range(self.max_retries):
            try:
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(output_file)
                return True
            except Exception as e:
                print(f'Edge TTS Error (Attempt {attempt + 1}/{self.max_retries}): {str(e)}')
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)
        return False