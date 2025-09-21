import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSizePolicy, QScrollArea, QGridLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, pyqtSignal

class CardWidget(QWidget):
    card_clicked = pyqtSignal()

    def __init__(self, image_path, id_text, name, created_at, parent=None):
        super(CardWidget, self).__init__(parent)
        # self.setMinimumSize(150, 150)  # 设置卡片的最小尺寸
        # self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)  # 设置大小策略

        self.is_selected = False

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

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Scrollable Card Example')
        self.setGeometry(100, 100, 800, 600)

        # 创建滚动区域
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # 创建滚动内容的容器
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        # 创建卡片布局
        grid_layout = QGridLayout()

        # 添加20个随机生成的卡片
        for i in range(20):
            card = CardWidget("test2.png", f"ID_{i}", f"Card {i}", "2024-06-11T12:00:00Z")
            row = i // 4  # 计算行号
            col = i % 4   # 计算列号
            grid_layout.addWidget(card, row, col)

        # 将卡片布局添加到滚动内容的垂直布局中
        self.scroll_layout.addLayout(grid_layout)

        # 设置滚动区域的内容
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)

        # 主窗口布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#
#     # 创建卡片窗口
#     card1 = CardWidget("test2.png", "1800764439778766850", "test", "2024-06-11T12:00:00Z")
#
#     # 创建一个主窗口并添加卡片
#     main_window = QWidget()
#     main_window.setWindowFlags(Qt.Window)
#     layout = QVBoxLayout()
#     # layout.setSpacing(10)  # 设置卡片之间的间隔
#     layout.addWidget(card1)
#     main_window.setLayout(layout)
#     main_window.show()
#
#     # 连接点击事件
#     card1.card_clicked.connect(lambda: print("Card clicked"))
#
#     sys.exit(app.exec_())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
