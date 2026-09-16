from PySide6.QtCore import QThread, Signal

class BackendThread(QThread):
    finished = Signal(object)
    error = Signal(str)

    def __init__(self, func):
        super().__init__()
        self.func = func

    def run(self):
        try:
            result = self.func()
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

