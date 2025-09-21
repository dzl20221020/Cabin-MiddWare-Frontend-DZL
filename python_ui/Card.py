import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSizePolicy, QScrollArea, QGridLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, pyqtSignal

class CardWidget(QWidget):
    card_clicked = pyqtSignal()

    def __init__(self, image_path, id_text, name,description,created_at, parent=None):
        super(CardWidget, self).__init__(parent)
        self.setFixedSize(260, 380)  # 设置卡片的最小尺寸

        self.is_selected = False

        self.image_path = image_path
        self.id_text = id_text
        self.name = name
        self.description = description
        self.created_at = created_at

        # 创建布局
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 添加封面图片
        cover_label = QLabel()
        pixmap = QPixmap(image_path)
        cover_label.setPixmap(pixmap.scaled(250, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        cover_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(cover_label)

        # 添加ID
        id_label = QLabel(f"ID: {id_text}")
        id_label.setFont(QFont("Arial", 10))
        id_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(id_label)

        # 添加名称
        name_label = QLabel(f"名称: {name}")
        name_label.setFont(QFont("Arial", 10))
        name_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(name_label)

        # 添加名称
        if description == None:
            description = ""
        description_label = QLabel(f"描述: {description}")
        description_label.setFont(QFont("Arial", 10))
        description_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(description_label)

        # 添加创建时间
        created_at_label = QLabel(f"创建时间: {created_at}")
        created_at_label.setFont(QFont("Arial", 10))
        created_at_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(created_at_label)

        self.mousePressEvent = self.handle_mouse_press
        self.update_style()

    def handle_mouse_press(self, event):
        self.is_selected = not self.is_selected
        self.update_style()
        self.card_clicked.emit()

    def update_style(self):
        if self.is_selected:
            self.setStyleSheet("""
                QWidget {
                    background-color: #2abb9c;
                    border-radius: 4px;
                    box-shadow: 0 12px 24px 0 rgba(0, 0, 0, 0.2);
                    padding: 10px;
                    transform: translateY(-12px);
                    transition: transform 0.3s, box-shadow 0.3s, background-color 0.3s;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #e4edec;
                    border-radius: 4px;
                    box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.1);
                    padding: 10px;
                    transform: translateY(0);
                    transition: transform 0.3s, box-shadow 0.3s, background-color 0.3s;
                }
            """)