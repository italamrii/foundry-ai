from PySide6.QtCore import QObject, Signal, Slot

from core.code_starter import CodeStarter


class CodeStarterWorker(QObject):
    finished = Signal(dict)
    failed = Signal(str)

    def __init__(self, blueprint, language):
        super().__init__()
        self.blueprint = blueprint
        self.language = language

    @Slot()
    def run(self):
        try:
            starter = CodeStarter()
            result = starter.generate(
                self.blueprint,
                self.language,
            )
            self.finished.emit(result)
        except Exception as exc:
            self.failed.emit(str(exc))