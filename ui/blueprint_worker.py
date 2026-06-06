from typing import Any, Dict
from PySide6.QtCore import QObject, Signal, Slot
from core.blueprint_engine import BlueprintEngine


class BlueprintWorker(QObject):
    finished = Signal(dict)
    failed = Signal(str)

    def __init__(self, idea: str, project_type: str, language: str) -> None:
        super().__init__()
        self.idea = idea
        self.project_type = project_type
        self.language = language

    @Slot()
    def run(self) -> None:
        try:
            engine = BlueprintEngine()
            blueprint: Dict[str, Any] = engine.generate(
                idea=self.idea,
                project_type=self.project_type,
                language=self.language,
            )
            self.finished.emit(blueprint)
        except Exception as exc:
            self.failed.emit(str(exc))
