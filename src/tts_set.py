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
        self.ttsProviderComboBox.clear()
        providers = ["Edge TTS", "其他TTS提供商"]
        self.ttsProviderComboBox.addItems(providers)
        self.ttsProviderComboBox.setCurrentText("Edge TTS")
        
        # 设置语种下拉框
        self.edgeTTSLanguageSet.clear()
        languages = ["中文", "韩语", "日语", "英语"]
        self.edgeTTSLanguageSet.addItems(languages)
        
        # 定义所有语音选项
        self.voices_mapping = {
            "中文": [
                {"name": "云健（男，普通话，热情）", "id": "zh-CN-YunjianNeural"},
                {"name": "云希（男，普通话，阳光）", "id": "zh-CN-YunxiNeural"},
                {"name": "云霄（男，普通话，可爱）", "id": "zh-CN-YunxiaNeural"},
                {"name": "云扬（男，普通话，专业）", "id": "zh-CN-YunyangNeural"},
                {"name": "万龙（男，粤语，友好）", "id": "zh-HK-WanLungNeural"},
                {"name": "云哲（男，台湾腔，友好）", "id": "zh-TW-YunJheNeural"},
                {"name": "晓晓（女，普通话，温暖）", "id": "zh-CN-XiaoxiaoNeural"},
                {"name": "晓伊（女，普通话，活力）", "id": "zh-CN-XiaoyiNeural"},
                {"name": "小北（女，东北话，幽默）", "id": "zh-CN-liaoning-XiaobeiNeural"},
                {"name": "小妮（女，陕西话，明亮）", "id": "zh-CN-shaanxi-XiaoniNeural"},
                {"name": "晓妍（女，粤语，友好）", "id": "zh-HK-HiuGaaiNeural"},
                {"name": "晓曼（女，粤语，友好）", "id": "zh-HK-HiuMaanNeural"},
                {"name": "晓陈（女，台湾腔，友好）", "id": "zh-TW-HsiaoChenNeural"},
                {"name": "晓语（女，台湾腔，友好）", "id": "zh-TW-HsiaoYuNeural"}
            ],
            "韩语": [
                {"name": "玄洙（男，友好）", "id": "ko-KR-HyunsuMultilingualNeural"},
                {"name": "仁俊（男，友好）", "id": "ko-KR-InJoonNeural"},
                {"name": "善熙（女，友好）", "id": "ko-KR-SunHiNeural"}
            ],
            "日语": [
                {"name": "圭太（男，友好）", "id": "ja-JP-KeitaNeural"},
                {"name": "七海（女，友好）", "id": "ja-JP-NanamiNeural"}
            ],
            "英语": [
                {"name": "Andrew（男，温暖）", "id": "en-US-AndrewNeural"},
                {"name": "Brian（男，随和）", "id": "en-US-BrianNeural"},
                {"name": "Christopher（男，可靠）", "id": "en-US-ChristopherNeural"},
                {"name": "Eric（男，理性）", "id": "en-US-EricNeural"},
                {"name": "Guy（男，热情）", "id": "en-US-GuyNeural"},
                {"name": "Roger（男，活力）", "id": "en-US-RogerNeural"},
                {"name": "Steffan（男，理性）", "id": "en-US-SteffanNeural"},
                {"name": "Ana（女，可爱）", "id": "en-US-AnaNeural"},
                {"name": "Aria（女，自信）", "id": "en-US-AriaNeural"},
                {"name": "Ava（女，友好）", "id": "en-US-AvaNeural"},
                {"name": "Emma（女，愉快）", "id": "en-US-EmmaNeural"},
                {"name": "Jenny（女，友好）", "id": "en-US-JennyNeural"},
                {"name": "Michelle（女，友好）", "id": "en-US-MichelleNeural"}
            ]
        }
        
        # 连接语种变化信号
        self.edgeTTSLanguageSet.currentTextChanged.connect(self.on_language_changed)
        
        # 初始化音色列表
        self.on_language_changed("中文")
        
    def on_language_changed(self, language):
        """处理语种变化"""
        self.edgeTTSVoiceSet.clear()
        if language in self.voices_mapping:
            voices = self.voices_mapping[language]
            self.edgeTTSVoiceSet.addItems([v["name"] for v in voices])
            self.voice_mapping = {v["name"]: v["id"] for v in voices}
    
    def on_tts_provider_changed(self, provider):
        # 处理TTS提供商变化
        if provider == "Edge TTS":
            self.ttsProviderStackedWidget.setCurrentIndex(0)  # 显示Edge TTS的设置页面
        elif provider == "其他TTS提供商":
            self.ttsProviderStackedWidget.setCurrentIndex(1)  # 显示其他提供商的设置页面
            
