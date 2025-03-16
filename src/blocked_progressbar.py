from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from src.ui.Ui_blocked_progressbar import Ui_Form

class BlockedProgressBar(QtWidgets.QWidget, Ui_Form):
    _instance = None
    
    def __new__(cls, parent=None):
        if cls._instance is None:
            cls._instance = super(BlockedProgressBar, cls).__new__(cls)
            super(BlockedProgressBar, cls._instance).__init__(parent)
        return cls._instance
    
    def __init__(self, parent=None):
        if not hasattr(self, '_initialized'):
            self.setupUi(self)
            self._initialized = True
            
            # 设置窗口标志
            self.setWindowFlags(QtCore.Qt.WindowType.Window | 
                              QtCore.Qt.WindowType.WindowStaysOnTopHint)
            
            # 连接按钮信号
            self.stopButton.clicked.connect(self.hide)
    
    @pyqtSlot(dict)
    def update_progress(self, data):
        if 'percentage' in data:
            percentage = data['percentage']
            self.progressBar.setValue(int(percentage))
            self.setWindowTitle(f"处理进度: {percentage:.1f}%")
            
            # 如果进度达到100%，自动隐藏窗口
            if percentage >= 100:
                self.hide()
                
    def showEvent(self, event):
        # 显示窗口时重置进度条
        self.progressBar.setValue(0)
        super().showEvent(event)