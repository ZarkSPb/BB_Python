from PySide6.QtWidgets import QWidget

from ui_rhytmwindow import Ui_RhytmWindow


class RhytmWindow(QWidget):
    def __init__(self, parent_ui):
        super(RhytmWindow, self).__init__()

        self.parent_ui = parent_ui

        self.ui = Ui_RhytmWindow()
        self.ui.setupUi(self)
    
    def closeEvent(self, event):
        self.parent_ui.actionRhytm_window.setChecked(False)