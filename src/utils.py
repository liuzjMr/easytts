import requests
from PyQt6.QtCore import QThread, pyqtSignal, QRunnable, QObject
from pathlib import Path
import chardet

class TTSWorker(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, text, service, config):
        super().__init__()
        self.text = text
        self.service = service
        self.config = config
    def run(self):
        try:
            response = requests.post('http://127.0.0.1:10032/api/tts', 
                                  json={"text": self.text, "service": self.service, "config": self.config})
            self.finished.emit(response.json())
        except Exception as e:
            self.error.emit(str(e))
        finally:
            # 任务完成后安排线程对象删除
            self.finished.connect(self.deleteLater)
            self.error.connect(self.deleteLater)


# 创建信号发射器
class TTSPoolWorkerSignals(QObject):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

class TTSPoolWorker(QRunnable):
    def __init__(self, text, service, config):
        super().__init__()
        self.text = text
        self.service = service
        self.config = config
        self.signals = TTSPoolWorkerSignals()
    
    def run(self):
        try:
            response = requests.post('http://127.0.0.1:10032/api/tts', 
                                  json={"text": self.text, "service": self.service, "config": self.config})
            self.signals.finished.emit(response.json())
        except Exception as e:
            self.signals.error.emit(str(e))


def get_text_from_file(input_file: str) -> str:
    def read_text_file(file_path):
        # 检测文件编码
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            detected = chardet.detect(raw_data)
            encoding = detected['encoding']
        
        try:
            # 使用检测到的编码读取文件
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except Exception as e:
            print(f"文件格式不支持: {e}")
            
    
    def read_epub_file(file_path):
        book = epub.read_epub(file_path)
        text = ""
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                text += soup.get_text() + "\n"
        return text
    
    def read_mobi_file(file_path):
        book = mobi.Mobi(file_path)
        return book.get_text()
    
    # 根据文件扩展名选择读取方式
    file_ext = Path(input_file).suffix.lower()
    if file_ext == '.epub':
        text = read_epub_file(input_file)
    elif file_ext == '.mobi':
        text = read_mobi_file(input_file)
    else:
        text = read_text_file(input_file)
        
    return text