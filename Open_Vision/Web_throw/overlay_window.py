import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPainter

from web_renderer import WebRenderer

class OverlayWindow(QMainWindow):
    trigger_web_signal = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        
        self.showFullScreen()
        
        self.web_renderer = WebRenderer()
        
        self.trigger_web_signal.connect(self.on_trigger_web)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)

    def on_trigger_web(self, x, y):
        self.web_renderer.add_web(x, y)

    def update_animation(self):
        self.web_renderer.update()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.web_renderer.draw(painter)
