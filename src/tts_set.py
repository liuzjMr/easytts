from PyQt6.QtWidgets import QWidget
from src.ui.Ui_tts_set import Ui_TTSSet
from src.utils import TTSWorker

class TTSSet(QWidget, Ui_TTSSet):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)
        
        # 连接信号和槽
        self.setup_connections()
        
        # 初始化UI
        self.init_ui()
        
    def setup_connections(self):
        # TTS提供商选择
        self.ttsProviderComboBox.currentTextChanged.connect(self.on_tts_provider_changed)
    
    def init_ui(self):
        # 设置 TTS 提供商下拉框
        self.ttsProviderComboBox.clear()  # 清空现有选项
        providers = ["Edge TTS", "其他TTS提供商"]
        self.ttsProviderComboBox.addItems(providers)
        self.ttsProviderComboBox.setCurrentText("Edge TTS")  # 设置默认选中项
        
        # 设置语种下拉框
        self.edgeTTSLanguageSet.clear()
        languages = ["中文", "英语", "日语", "韩语"]
        self.edgeTTSLanguageSet.addItems(languages)
        
        # 设置音色下拉框
        self.edgeTTSVoiceSet.clear()
        voices = [
            {"name": "晓晓（女）", "id": "zh-CN-XiaoxiaoNeural"},
            {"name": "云扬（男）", "id": "zh-CN-YunyangNeural"},
            {"name": "云希（男）", "id": "zh-CN-YunxiNeural"},
            {"name": "晓伊（女）", "id": "zh-CN-XiaoyiNeural"}
        ]
        self.edgeTTSVoiceSet.addItems([v["name"] for v in voices])
        self.voice_mapping = {v["name"]: v["id"] for v in voices}
    
    def on_tts_provider_changed(self, provider):
        # 处理TTS提供商变化
        if provider == "Edge TTS":
            self.ttsProviderStackedWidget.setCurrentIndex(0)  # 显示Edge TTS的设置页面
        elif provider == "其他TTS提供商":
            self.ttsProviderStackedWidget.setCurrentIndex(1)  # 显示其他提供商的设置页面
            
