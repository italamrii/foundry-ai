from PySide6.QtCore import QObject, Signal, Slot

from core.github_planner import GitHubPlanner


class GitHubPlannerWorker(QObject):
    finished = Signal(dict)
    failed = Signal(str)

    def __init__(self, blueprint: dict, language: str) -> None:
        super().__init__()
        self.blueprint = blueprint
        self.language = language

    @Slot()
    def run(self) -> None:
        try:
            planner = GitHubPlanner()
            result = planner.generate(self.blueprint, self.language)
            self.finished.emit(result)
        except Exception as exc:
            self.failed.emit(str(exc))