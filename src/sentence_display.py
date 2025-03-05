from PyQt6.QtWidgets import QWidget, QMessageBox, QDialog
from src.ui.Ui_sentence_display import Ui_sentenceDisplay
from src.tts_set_dialog import TTSSetDialog
import os
import json
from src.utils import TTSWorker

class SentenceDisplay(QWidget, Ui_sentenceDisplay):
    def __init__(self, parent=None, sentence_text:str="", sentence_index:int =0):
        super().__init__(parent)
        self.setupUi(self)
        self.sentence_text = sentence_text
        self.sentence_index = sentence_index
        self.audio_path = None
        
        # 设置句子文本
        self.sentenceTextBrowser.setText(sentence_text)
        self.sentenceIdLabel.setText(str(self.sentence_index))
        
        # 连接信号和槽
        self.sentenceSetButton.clicked.connect(self.on_tts_settings_clicked)
        
    def on_tts_settings_clicked(self):
        """处理TTS设置按钮点击事件"""
        # 创建并显示TTS设置对话框，传入当前句子文本
        self.dialog = TTSSetDialog(self, text=self.sentence_text)  # 保存为实例变量
        self.dialog.finished.connect(lambda result: self.handle_dialog_finished(self.dialog, result))
        self.dialog.show()
        
    def handle_dialog_finished(self, dialog, result):
        """处理对话框关闭事件"""
        if result == QDialog.DialogCode.Accepted and hasattr(dialog, 'result'):
            # 生成成功，更新音频路径
            self.audio_path = dialog.result['audio_url']
            # 更新音频播放器
            self.sentencePlyer.load_audio(self.audio_path)
