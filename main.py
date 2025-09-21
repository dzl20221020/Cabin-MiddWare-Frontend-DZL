import os
import sys
import threading
import time
import traceback
import win32con
import win32gui
import win32process
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QWidget, QApplication, QPushButton, QVBoxLayout

from component.notification import NotificationManager
from entity.Student import Student
from python_ui.Window1 import Window1
from python_ui.Window2 import Window2
from python_ui.Window3 import Window3
import global_vars
from python_ui.Window4 import Window4
from python_ui.Window5 import Window5
from service.experimenstatusmanager import ExperimentWebSocketClient

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     MainWindow = QMainWindow()
#     ui = MainWindow2()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.resize(1920, 1080)
        self.move(0, 0)

        # 创建 QStackedWidget
        self.stackedWidget = QStackedWidget()
        self.setCentralWidget(self.stackedWidget)

        # 创建页面
        self.window1 = Window1(self.stackedWidget)
        self.window2 = Window2(self.stackedWidget)
        self.window3 = Window3(self.stackedWidget)
        self.window4 = Window4(self.stackedWidget)
        self.window5 = Window5(self.stackedWidget)

        # 信号与槽绑定
        self.window1.startExperiment_signal.connect(self.toWindow2)
        self.window2.toWindow1_signal.connect(self.toWindow1)
        self.window2.toWindow3_signal.connect(self.toWindow3)
        self.window3.toWindow2_signal.connect(self.toWindow2)
        self.window3.toWindow4_signal.connect(self.toWindow4)
        self.window4.toWindow3_signal.connect(self.toWindow3)
        self.window4.toWindow5_signal.connect(self.toWindow5)
        self.window5.toWindow4_signal.connect(self.toWindow4)

        # 添加页面到 QStackedWidget
        self.stackedWidget.addWidget(self.window1)
        self.stackedWidget.addWidget(self.window2)
        self.stackedWidget.addWidget(self.window3)
        self.stackedWidget.addWidget(self.window4)
        self.stackedWidget.addWidget(self.window5)

        # 显示第一个页面
        self.stackedWidget.setCurrentIndex(0)

        self.experimentWebsocketClient = ExperimentWebSocketClient()
        self.experimentWebsocketClient.data_received.connect(self.experimentStatusManager)
        self.experimentWebsocketClient.start()

    # 用于在实验不同阶段进行不同的处理

    def experimentStatusManager(self,message):
        # 使用 split() 方法按空格分隔字符串
        messageArr = message.split()
        global_vars.experiment_status = messageArr[1]

        if (messageArr[1] == "ENDED"):
            # 把页面返回至最开始页面
            self.stackedWidget.setCurrentIndex(0)
            # 清空学生信息
            global_vars.student = Student("", "", "", 0, 0, 0)
            # 清空范式选择
            global_vars.paradigm_id = None
            # 清空实验id
            global_vars.experiment_id = None
            # 轻控股状态
            global_vars.experiment_status = None
            # 启动开始实验按钮
            self.window5.beginBtn.setEnabled(True)
        if (messageArr[1] == "TERMINATED"):
            # 提示系统未正常工作，正在进行系统初始化，请等待系统初始化完成
            NotificationManager.show_notification(
                self,
                title="警告",
                message="检测到系统未正常工作，系统即将异常重置，请耐心等待系统重置完成",
                auto_close=True,
                timeout=10000
            )

            # 设置定时器，等待通知结束再执行后续操作
            QTimer.singleShot(10000, self.reset_system)



    def reset_system(self):
        # 把页面返回至最开始页面
        self.stackedWidget.setCurrentIndex(0)
        # 清空学生信息
        global_vars.student = Student("", "", "", 0, 0, 0)
        # 清空范式选择
        global_vars.paradigm_id = None
        # 清空实验id
        global_vars.experiment_id = None
        # 轻控股状态
        global_vars.experiment_status = None
        # 启动开始实验按钮
        self.window5.beginBtn.setEnabled(True)


    def toWindow2(self):
        self.stackedWidget.setCurrentIndex(1)
        self.window2.updateForm()

    def toWindow1(self):
        self.stackedWidget.setCurrentIndex(0)

    def toWindow3(self):
        self.stackedWidget.setCurrentIndex(2)
        self.embed_gazepoint()

    def toWindow4(self):
        self.stackedWidget.setCurrentIndex(3)
        self.window4.getAllParadigm()
    def toWindow5(self):
        self.stackedWidget.setCurrentIndex(4)
        self.window5.initUserInfo()
        self.window5.initParadigmInfoTable()
    def start_gazepoint(self):
        try:
            global_vars.gazepoint_hwnd = self.start_external_application("C:\\Program Files (x86)\\Gazepoint\\Gazepoint\\bin64\\Gazepoint.exe")
        except Exception as e:
            print(f"Failed to start application: {e}")

    def start_external_application(self, application_path):
        if not os.path.isfile(application_path) and not self.find_in_path(application_path):
            raise FileNotFoundError(f"The application '{application_path}' was not found.")

        startup_info = win32process.STARTUPINFO()
        process_info = win32process.CreateProcess(application_path, None, None, None, False, 0, None, None, startup_info)
        process_handle = process_info[0]
        global_vars.gazepoint_pid = win32process.GetProcessId(process_handle)
        print(f"Started process with handle: {process_handle} and PID: {global_vars.gazepoint_pid}")

        # 启动检查弹窗的线程
        popup_checker_thread = threading.Thread(target=self.run_popup_checker, args=(global_vars.gazepoint_pid,))
        popup_checker_thread.daemon = True
        popup_checker_thread.start()

        time.sleep(5)  # 调整等待时间

        hwnd = self.get_main_window_hwnd(global_vars.gazepoint_pid)
        if hwnd:
            print(f"Found main window handle: {hwnd}")
            # self.maximize_window(hwnd)
        else:
            print("No main window handle found.")
        return hwnd

    def find_in_path(self, executable):
        for path in os.environ["PATH"].split(os.pathsep):
            full_path = os.path.join(path, executable)
            if os.path.isfile(full_path):
                return full_path
        return None

    def get_main_window_hwnd(self, pid):
        def enum_windows_callback(hwnd, hwnds):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid and "gazepoint control" in win32gui.GetWindowText(hwnd).lower():
                hwnds.append(hwnd)
            return True

        hwnds = []
        win32gui.EnumWindows(enum_windows_callback, hwnds)
        return hwnds[0] if hwnds else None

    def embed_gazepoint(self):
        if global_vars.gazepoint_hwnd:
            print(f"Embedding window handle: {global_vars.gazepoint_hwnd}")
            try:
                win32gui.SetParent(global_vars.gazepoint_hwnd, self.window3.gazepointWidget.winId())
                win32gui.SetWindowLong(global_vars.gazepoint_hwnd, win32con.GWL_STYLE,
                                       win32gui.GetWindowLong(global_vars.gazepoint_hwnd,
                                                              win32con.GWL_STYLE) | win32con.WS_CHILD)
                self.adjust_gazepoint_size()
            except Exception as e:
                print(f"Failed to embed window: {e}")

    def adjust_gazepoint_size(self):
        if global_vars.gazepoint_hwnd:
            rect = self.window3.gazepointWidget.geometry()
            win32gui.SetWindowPos(global_vars.gazepoint_hwnd, win32con.HWND_TOP, 0, 0, rect.width(), rect.height(), win32con.SWP_SHOWWINDOW)

    def maximize_window(self, hwnd):
        # 最大化窗口
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

    def check_for_popup(self, pid):
        def enum_windows_callback(hwnd, hwnds):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                window_title = win32gui.GetWindowText(hwnd)
                class_name = win32gui.GetClassName(hwnd)
                if win32gui.GetParent(hwnd) != 0:  # 仅处理子窗口
                    print(f"Detected popup window with title: {window_title}, class: {class_name}")  # 调试信息
                    hwnds.append(hwnd)
            return True

        hwnds = []
        win32gui.EnumWindows(enum_windows_callback, hwnds)
        if hwnds:
            for hwnd in hwnds:
                print(
                    f"Found popup window: {hwnd} with title: {win32gui.GetWindowText(hwnd)}, class: {win32gui.GetClassName(hwnd)}")
                # 点击确定按钮
                win32gui.SetForegroundWindow(hwnd)
                time.sleep(0.5)  # 等待窗口聚焦
                win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
                win32gui.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
                print("Popup closed.")
            return True  # 表示已经找到并处理了弹窗
        else:
            print("No popup window found.")  # 调试信息
        return False  # 表示没有找到弹窗

    def run_popup_checker(self, pid):
        while True:
            if self.check_for_popup(pid):
                break  # 检测到弹窗并处理后，停止检测
            time.sleep(1)  # 每秒检查一次





if __name__ == '__main__':
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        error_message = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        print(f"Unhandled exception: {error_message}")

        try:
            experimentWebsocketClient = ExperimentWebSocketClient()
            experimentWebsocketClient.start()
            if experimentWebsocketClient:
                if global_vars.experiment_id is None:
                    experiment_id = ""
                else:
                    experiment_id = global_vars.experiment_id
                experimentWebsocketClient.send_data(experiment_id + " TERMINATED")
        except Exception as e:
            print(f"Failed to send WebSocket message: {e}")

        try:
            restart_application()
        except Exception as e:
            print(f"Failed to restart application: {e}")

            # 显示通知
            NotificationManager.show_notification(
                title="警告",
                message="检测到系统未正常工作，系统即将异常重置，请耐心等待系统重置完成",
                auto_close=True,
                timeout=10000  # 10秒钟自动关闭通知
            )

            # 使用 QTimer 延迟重启
            QTimer.singleShot(10000, restart_application)  # 等待 10 秒再重启


    def restart_application():
        import os
        import sys
        import subprocess
        import time

        script_path = os.path.abspath(sys.argv[0])
        print(f"Restarting application: {script_path}")

        # 启动新的进程并等待一段时间
        subprocess.Popen([sys.executable, script_path])
        time.sleep(2)  # 确保新进程有时间启动

        sys.exit()

    sys.excepthook = handle_exception
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    # 开启gazepointcontrol软件
    main.start_gazepoint()
    sys.exit(app.exec_())
