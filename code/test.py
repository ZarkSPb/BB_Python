from brainflow.board_shim import BoardIds, BoardShim, BrainFlowInputParams
from PySide6.QtCore import QTimer
from PySide6 import QtGui

BOARD_ID = BoardIds.SYNTHETIC_BOARD.value
# BOARD_ID = BoardIds.BRAINBIT_BOARD.value


class Gr:
    def __init__(self, board):
        self.board = board

        self.app = QtGui.QGuiApplication([])
        self.app.setQuitOnLastWindowClosed(False)        

        timer = QTimer()
        timer.timeout.connect(self.update)
        timer.start(20)

        self.i = 0

        self.app.exec()

    def update(self):
        while self.i < 3000:
            data = self.board.get_board_data_count()
            print(self.i, data)
            self.i += 1

def main():
    BoardShim.enable_dev_board_logger()
    params = BrainFlowInputParams()
    try:
        board = BoardShim(BOARD_ID, params)
        board.prepare_session()
        board.start_stream(450000)

        g = Gr(board)

    finally:
        if board.is_prepared():
            board.release_session()

if __name__ == "__main__":
    main()

i = 0
while i < 10:
    data = board.get_current_board_data(2)
    if np.any(data):
        i += 1
        # print(i, j, data, "\n\n")
        # data = np.array([[]])
        print(i, data)
        print('---------', j)
        j = 0
    j += 1

# import sys

# from PySide6.QtCore import QTimer
# from PySide6.QtGui import QGuiApplication

# app = QGuiApplication(sys.argv)
# app.setQuitOnLastWindowClosed(False)

# def tick():
#     print('tick')

# timer = QTimer()
# timer.timeout.connect(tick)
# timer.start(1000)

# # run event loop so python doesn't exit
# app.exec()