import sys
from PySide6.QtWidgets import QApplication
from app.startup import bootstrap_app
from ui.main_window import MainWindow


def main() -> None:
    bootstrap_app()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
