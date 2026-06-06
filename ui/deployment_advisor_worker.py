from PySide6.QtCore import QObject, Signal, Slot

from core.deployment_advisor import DeploymentAdvisor


class DeploymentAdvisorWorker(QObject):
    finished = Signal(dict)
    failed = Signal(str)

    def __init__(self, blueprint: dict, language: str):
        super().__init__()
        self.blueprint = blueprint
        self.language = language

    @Slot()
    def run(self):
        try:
            advisor = DeploymentAdvisor()
            result = advisor.generate(self.blueprint, self.language)
            self.finished.emit(result)
        except Exception as exc:
            self.failed.emit(str(exc))