import sys
import traceback

from PySide6.QtCore import QObject, QRunnable, Signal, Slot


class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @Slot()  #QtCore.Slot
    def run(self):
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            extype, value = sys.exc_info()[:2]
            self.signals.error.emit((extype, value, traceback.format_exc()))
        else:
            # Return the result of the processing
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()  # Done