import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QFrame
from PyQt5.QtCore import Qt, QTimer, QRect, QSize
from PyQt5.QtGui import QPainter, QColor, QFont, QPen

class CircularLoadingAnimation(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Circular Loading Animation")
        self.setGeometry(100, 100, 600, 600)

        # 创建主布局
        main_layout = QVBoxLayout()

        # 创建内容区域
        self.content_area = QWidget()
        content_layout = QVBoxLayout(self.content_area)
        # 在这里添加您的应用程序内容

        # 创建加载动画区域
        self.loading_area = QWidget()
        loading_layout = QVBoxLayout(self.loading_area)
        loading_layout.setAlignment(Qt.AlignCenter)

        # 创建自定义 QLabel 来绘制圆形加载动画
        self.loading_label = CustomLoadingLabel(self)
        self.loading_label.setFixedSize(150, 150)

        # 创建遮罩层
        self.mask_frame = QFrame(self.loading_area)
        self.mask_frame.setStyleSheet("background-color: rgba(255, 255, 255, 0.8);")
        self.mask_frame.setGeometry(0, 0, self.size().width(), self.size().height())

        # 将加载动画 Label 和遮罩层添加到加载动画区域
        loading_layout.addWidget(self.loading_label)
        loading_layout.addWidget(self.mask_frame)

        # 将内容区域和加载动画区域添加到主布局
        main_layout.addWidget(self.content_area)
        main_layout.addWidget(self.loading_area)

        # 创建一个容器 widget 并设置布局
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # 启动加载动画
        self.loading_label.start_loading_animation()

class CustomLoadingLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.progress = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)

    def start_loading_animation(self):
        self.timer.start(50)  # 每 50 毫秒更新一次进度

    def update_progress(self):
        self.progress = (self.progress + 3) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制外圈
        painter.setPen(QPen(QColor(230, 230, 230), 6))
        painter.drawEllipse(QRect(15, 15, 120, 120))

        # 绘制进度圆弧
        painter.setPen(QPen(QColor(150, 150, 150), 6))
        painter.drawArc(QRect(15, 15, 120, 120), (self.progress - 90) * 16, 270 * 16)

        # 绘制中间文字
        painter.setFont(QFont("Arial", 16))
        painter.drawText(self.rect(), Qt.AlignCenter, "Loading...")