import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer

class AutoCloseMessageBox:
    def __init__(self,parent,icon, title, message, timeout=3000):
        super(AutoCloseMessageBox, self).__init__(parent)
        self.msg_box = QMessageBox()
        self.msg_box.setIcon(icon)
        self.msg_box.setWindowTitle(title)
        self.msg_box.setText(message)
        self.msg_box.setStandardButtons(QMessageBox.Ok)

        # 使用定时器在指定时间后关闭消息框
        QTimer.singleShot(timeout, self.msg_box.close)

    def show(self):
        self.msg_box.exec_()