from typing import Optional
from src.client.base_client import BaseClient
from src.client.edge_tts_client import EdgeTTSClient

class ClientFactory:
    """TTS 服务工厂"""
    _clients = {}
    @classmethod
    def register(cls, name: str, client_class: type):
        """注册 TTS 客户端"""
        cls._clients[name] = client_class
    
    @classmethod
    def create(cls, name: str, **kwargs) -> Optional[BaseClient]:
        """创建 TTS 客户端实例"""
        if name not in cls._clients:
            return None
        return cls._clients[name](**kwargs)
    
# 注册 Edge TTS 客户端
ClientFactory.register('edge-tts', EdgeTTSClient)