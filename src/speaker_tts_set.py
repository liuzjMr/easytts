from PyQt6.QtWidgets import QWidget
from src.ui.Ui_speaker_tts_set import Ui_speakerTTSSet
from src.tts_set_dialog import TTSSetDialog

class SpeakerTTSSet(QWidget, Ui_speakerTTSSet):
    def __init__(self, parent=None, speaker_name=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # 初始化属性
        self.speaker_name = speaker_name
        self.service = "Edge TTS"
        self.config = {"language": "中文", "voice_name": "晓晓（女，普通话，温暖）"}
        
        # 设置说话人标签
        self.speakerLabel.setText(speaker_name)
        self.speakerSetButton.setText("角色TTS设置")
        
        # 连接按钮信号
        self.speakerSetButton.clicked.connect(self.show_tts_dialog)
        
    def show_tts_dialog(self):
        """显示TTS设置对话框"""
        dialog = TTSSetDialog(self, speaker=self.speaker_name)
        
        # 如果已有设置，则设置到对话框中
        if self.service and self.config:
            dialog.widget.ttsProviderComboBox.setCurrentText(self.service)
            dialog.widget.edgeTTSLanguageSet.setCurrentText(self.config['language'])
            dialog.widget.edgeTTSVoiceSet.setCurrentText(self.config['voice_name'])
        
        if dialog.exec():
            # 保存设置
            self.service = dialog.service
            self.config = dialog.config
            