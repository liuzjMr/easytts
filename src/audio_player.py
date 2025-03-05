from PyQt6.QtWidgets import QWidget, QFileDialog, QStyle
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from src.ui.Ui_audio_player import Ui_audioPlayer
import os
import shutil

        
class AudioPlayer(QWidget, Ui_audioPlayer):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.audio_path = None
        
        # 初始化播放器
        self.setup_player()
        # 连接信号和槽
        self.setup_connections()
        # 初始化UI
        self.init_ui()
        
    def setup_player(self):
        """初始化播放器"""
        self.player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.player.setAudioOutput(self.audio_output)
        
    def setup_connections(self):
        """设置信号连接"""
        # 播放控制
        self.playButton.clicked.connect(self.play_pause)
        # 播放状态改变控制
        self.player.playbackStateChanged.connect(self.on_playback_state_changed)
        
        # 音量控制
        self.volumeButton.clicked.connect(self.toggle_volume_control)
        self.volumeSlider.valueChanged.connect(self.on_volume_changed)

        # 下载按钮
        self.downloadButton.clicked.connect(self.download_audio)
        
        # 进度条
        self.timeSlider.sliderMoved.connect(self.seek)
        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(self.update_duration)
        
        # 播放速度控制
        self.speedButton.clicked.connect(self.toggle_speed_control)
        self.speedSpinBox.valueChanged.connect(self.on_speed_changed)
        
    def init_ui(self):
        """初始化界面"""
        self.currentTimeLabel.setText("00:00")
        self.totalTimeLabel.setText("00:00")
        # 初始隐藏音量控制组件
        self.volumeSlider.hide()
        self.volumeLabel.hide()
        self.speedSpinBox.hide()
        self.textBrowser.hide()
    
    def load_audio(self, file_path):
        """加载音频文件"""
        if os.path.exists(file_path):
            self.audio_path = file_path
            self.player.setSource(QUrl.fromLocalFile(file_path))
            return True
        return False
    
    def seek(self, position):
        """跳转到指定位置"""
        self.player.setPosition(position)
        
    def update_position(self, position):
        """更新当前播放位置"""
        self.timeSlider.setValue(position)
        self.currentTimeLabel.setText(self.format_time(position))
        
    def update_duration(self, duration):
        """更新总时长"""
        self.timeSlider.setRange(0, duration)
        self.totalTimeLabel.setText(self.format_time(duration))
        
    def play_pause(self):
        """播放/暂停切换"""
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
            self.playButton.setChecked(False)
            # 设置播放图标
            self.playButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        else:
            self.player.play()
            self.playButton.setChecked(True)
            # 设置暂停图标
            self.playButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))

    def on_playback_state_changed(self, state):
        """处理播放状态变化"""
        if state == QMediaPlayer.PlaybackState.StoppedState:
            self.playButton.setChecked(False)
            self.playButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
    def format_time(self, ms):
        """格式化时间显示"""
        s = ms // 1000
        m = s // 60
        s = s % 60
        return f"{m:02d}:{s:02d}"
    def toggle_volume_control(self):
        """切换音量控制显示状态"""
        if self.volumeSlider.isVisible():
            self.volumeSlider.hide()
            self.volumeLabel.hide()
        else:
            self.volumeSlider.show()
            self.volumeLabel.show()
            # 设置当前音量值
            current_volume = int(self.audio_output.volume() * 100)
            self.volumeSlider.setValue(current_volume)
            self.volumeLabel.setText(f"{current_volume}%")
            
    def on_volume_changed(self, value):
        """处理音量变化"""
        volume = value / 100.0
        self.audio_output.setVolume(volume)
        self.volumeLabel.setText(f"{value}%")
        
    def download_audio(self):
        """下载音频文件"""
        if not self.audio_path:
            return
            
        file_name = os.path.basename(self.audio_path)
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存音频文件",
            file_name,
            "音频文件 (*.mp3 *.wav);;所有文件 (*.*)"
        )
        
        if save_path:
            try:
                shutil.copy2(self.audio_path, save_path)
            except Exception as e:
                print(f"下载失败：{str(e)}")
                
    def toggle_speed_control(self):
        """切换播放速度控制显示状态"""
        if self.speedSpinBox.isVisible():
            self.speedSpinBox.hide()
        else:
            self.speedSpinBox.show()
            # 设置当前速度值
            current_rate = self.player.playbackRate()
            self.speedSpinBox.setValue(current_rate)
            
    def on_speed_changed(self, value):
        """处理播放速度变化"""
        self.player.setPlaybackRate(value)