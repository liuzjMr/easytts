from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt
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
        self.voice_display_name = "未设置"
        
        # 设置说话人标签
        self.speakerLabel.setText(speaker_name)
        self.speakerSetButton.setText("角色TTS设置")
        
        # 初始化界面
        self.init_ui()
        
        # 连接按钮信号
        self.speakerSetButton.clicked.connect(self.show_tts_dialog)
        
    def init_ui(self):
        # 创建音色显示标签
        self.voiceNameLabel = QLabel(self.voice_display_name)
        self.voiceNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 清除现有布局并创建新的水平布局
        while self.horizontalLayout.count():
            item = self.horizontalLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
        
        # 添加到新的水平布局中
        self.horizontalLayout.addWidget(self.speakerLabel, 1)
        self.horizontalLayout.addWidget(self.voiceNameLabel, 2)
        self.horizontalLayout.addWidget(self.speakerSetButton, 1)
        
        # 设置边距和间距
        self.horizontalLayout.setContentsMargins(10, 8, 10, 8)
        self.horizontalLayout.setSpacing(8)
        
    def show_tts_dialog(self):
        """显示TTS设置对话框"""
        dialog = TTSSetDialog(self, speaker=self.speaker_name)
        
        # 如果已有设置，则设置到对话框中
        if self.service and self.config:
            dialog.widget.ttsProviderComboBox.setCurrentText(self.service)
            dialog.widget.edgeTTSLanguageSet.setCurrentText(self.config['language'])
            dialog.widget.edgeTTSVoiceSet.setCurrentText(self.config['voice_name'])

        # 如果对话框被接受
        if dialog.exec() == TTSSetDialog.DialogCode.Accepted:
            if hasattr(dialog, 'service') and hasattr(dialog, 'config'):
                # 获取对话框中设置的TTS配置
                self.service = dialog.service
                self.config = dialog.config
                
                # 更新音色显示名称
                if 'voice_name' in dialog.config:
                    self.voice_display_name = dialog.config['voice_name']
                else:
                    self.voice_display_name = "默认语音"
                
                # 更新UI显示
                self.voiceNameLabel.setText(self.voice_display_name)
