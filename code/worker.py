from PySide6.QtCore import QObject, Signal, QThread


class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)


class Worker(QThread):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    # @Slot()  #QtCore.Slot
    def run(self):
        self.fn(*self.args, **self.kwargs)