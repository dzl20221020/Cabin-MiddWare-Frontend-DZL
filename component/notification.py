import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QGraphicsOpacityEffect
from PyQt5.QtCore import QTimer, Qt, QPoint, QPropertyAnimation, QEasingCurve


class Notification(QWidget):
    def __init__(self, title, message, auto_close=True, timeout=3000, parent=None):
        super(Notification, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.init_ui(title, message)

        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(500)
        self.fade_animation.setStartValue(1)
        self.fade_animation.setEndValue(0)
        self.fade_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_animation.finished.connect(self.close_notification)

        if auto_close:
            QTimer.singleShot(timeout, self.start_fade_out)

        self.slide_animation = QPropertyAnimation(self, b"pos")
        self.slide_animation.setDuration(500)

    def init_ui(self, title, message):
        layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")

        message_label = QLabel(message)
        message_label.setStyleSheet("color: teal;")

        layout.addWidget(title_label)
        layout.addWidget(message_label)

        self.setLayout(layout)
        self.adjustSize()

    def show(self, start_pos, end_pos):
        self.move(start_pos)
        super().show()

        self.slide_animation.setStartValue(start_pos)
        self.slide_animation.setEndValue(end_pos)
        self.slide_animation.start()

    def start_fade_out(self):
        self.fade_animation.start()

    def close_notification(self):
        NotificationManager.remove_notification(self)
        self.close()


class NotificationManager:
    notifications = []

    @staticmethod
    def show_notification(parent, title, message, auto_close=True, timeout=3000):
        notification = Notification(title, message, auto_close, timeout, parent)

        screen_geometry = parent.geometry()
        start_pos = QPoint(screen_geometry.width(),
                           10 + len(NotificationManager.notifications) * (notification.height() + 10))
        end_pos = QPoint(screen_geometry.width() - notification.width() - 10,
                         10 + len(NotificationManager.notifications) * (notification.height() + 10))

        notification.show(start_pos, end_pos)
        NotificationManager.notifications.append(notification)

    @staticmethod
    def remove_notification(notification):
        if notification in NotificationManager.notifications:
            NotificationManager.notifications.remove(notification)
            NotificationManager.reposition_notifications()

    @staticmethod
    def reposition_notifications():
        for i, notification in enumerate(NotificationManager.notifications):
            end_pos = QPoint(notification.parent().geometry().width() - notification.width() - 10,
                             10 + i * (notification.height() + 10))
            notification.slide_animation.setStartValue(notification.pos())
            notification.slide_animation.setEndValue(end_pos)
            notification.slide_animation.start()
