from PyQt6.QtWidgets import QDialog, QMessageBox, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from src.ui.Ui_tts_set_dialog import Ui_TTSSetDialog
from src.utils import TTSWorker

class TTSSetDialog(QDialog, Ui_TTSSetDialog):
    def __init__(self, parent=None, text=None, speaker=None):
        super().__init__(parent)
        self.setupUi(self)
        self.text = text  # 保存要转换的文本
        self.speaker = speaker  # 保存说话人信息
        
        # 连接生成按钮的信号
        self.widget.generateButton.clicked.connect(self.on_generate_clicked)
        # 链接保存按钮的信号
        self.widget.saveSetButton.clicked.connect(self.on_save_clicked)
        # 初始化UI
        self.init_ui()
        
    def on_generate_clicked(self):
        # 获取当前设置
        service = self.widget.ttsProviderComboBox.currentText()
        voice_name = self.widget.edgeTTSVoiceSet.currentText()
        voice_id = self.widget.voice_mapping[voice_name]
        config = {"voice": voice_id}
        
        # 禁用生成按钮，避免重复点击
        self.widget.generateButton.setEnabled(False)
        
        # 创建工作线程生成语音
        self.worker = TTSWorker(self.text, service, config)
        self.worker.finished.connect(self.handle_tts_result)
        self.worker.error.connect(self.handle_tts_error)
        self.worker.start()
        
        
        
    def handle_tts_result(self, result):
        self.widget.generateButton.setEnabled(True)
        if result['success']:
            # 关闭对话框并返回结果
            self.result = result
            self.accept()
        else:
            QMessageBox.warning(self, "生成失败", f"语音生成失败：{result.get('error', '未知错误')}")
            
    def handle_tts_error(self, error):
        self.widget.generateButton.setEnabled(True)
        QMessageBox.critical(self, "生成错误", f"语音生成错误：{error}")
        
    def on_save_clicked(self):
        # 获取当前设置
        service = self.widget.ttsProviderComboBox.currentText()
        language = self.widget.edgeTTSLanguageSet.currentText()
        voice_name = self.widget.edgeTTSVoiceSet.currentText()
        voice_id = self.widget.voice_mapping[voice_name]
        config = {"voice": voice_id,"voice_name": voice_name,"language": language}

        # 保存设置到对话框属性中
        self.service = service
        self.config = config
        
        # 关闭对话框，返回接受结果
        self.accept()

    def init_ui(self):
        # 设置窗口标题
        if self.speaker:
            self.setWindowTitle(f"为角色 [{self.speaker}] 设置 TTS")
            
            # 添加标题标签显示当前设置的角色
            titleLabel = QLabel(f"为角色 [{self.speaker}] 设置 TTS 参数")
            titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            font = titleLabel.font()
            font.setPointSize(12)
            font.setBold(True)
            titleLabel.setFont(font)
            
            # 将标题标签添加到现有布局的顶部
            # 首先检查是否已有布局
            mainLayout = self.layout()
            if mainLayout:
                # 在已有的布局中插入标题标签
                mainLayout.insertWidget(0, titleLabel)
            else:
                # 如果没有布局，创建一个新的垂直布局
                mainLayout = QVBoxLayout(self)
                mainLayout.addWidget(titleLabel)
                mainLayout.addWidget(self.widget)
                self.setLayout(mainLayout)
            
        # 根据不同模式显示不同按钮
        if self.text:
            # 语音生成模式，不展示saveSetButton
            self.widget.saveSetButton.hide()
        else:
            # 设置模式，不展示generateButton
            self.widget.generateButton.hide()
            # 显示saveSetButton
            self.widget.saveSetButton.show()
            
    def closeEvent(self, event):
        """重写关闭事件"""
        if hasattr(self, 'worker') and self.worker and self.worker.isRunning():
            # 如果线程正在运行，阻止关闭
            event.ignore()
            QMessageBox.warning(self, "警告", "正在生成音频，请等待完成...\n但你可以点击主窗口其他句子的TTS设置按钮，来多线程地生成其他句子的音频。")