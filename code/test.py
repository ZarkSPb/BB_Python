import sys
import threading
from PySide6.QtCore import QThread, QTimer
from PySide6.QtWidgets import QApplication, QPushButton, QWidget


class WorkerThread(QThread):
    def run(self):
        def work():
            print("working from :" + str(threading.get_ident()))
            QThread.sleep(5)
        print("thread started from :" + str(threading.get_ident()))
        timer = QTimer()
        timer.timeout.connect(work)
        timer.start(1000)
        self.exec()

class MyGui(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.worker = WorkerThread(self)
        print("Starting worker from :" + str(threading.get_ident()))
        self.worker.start()

    def initUi(self):
        self.setGeometry(500, 500, 300, 300)
        self.pb = QPushButton("Button", self)
        self.pb.move(50, 50)


if __name__ == '__main__':    
    app = QApplication(sys.argv)
    gui = MyGui()
    gui.show()
    sys.exit(app.exec())