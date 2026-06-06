from PySide6.QtCore import Qt, QThread, Slot
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.config import PROJECT_TYPES
from app.constants import APP_NAME
from app.translations import t
from core.project_manager import ProjectManager
from core.validators import validate_project_idea
from exporters.pdf_exporter import PDFExporter
from ui.blueprint_tabs import BlueprintTabs
from ui.blueprint_worker import BlueprintWorker
from ui.architecture_worker import ArchitectureWorker
from ui.github_planner_worker import GitHubPlannerWorker
from ui.deployment_advisor_worker import DeploymentAdvisorWorker
from ui.code_starter_worker import CodeStarterWorker
from PySide6.QtWidgets import QMessageBox

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.language = "ar"
        self.setWindowTitle(APP_NAME)
        self.resize(1400, 850)

        self.blueprint = None
        self.project_id = None
        self.thread = None
        self.worker = None
        self.project_manager = ProjectManager()
        self.pdf_exporter = PDFExporter()
        self.pending_idea = ""
        self.pending_project_type = ""

        self.header = QLabel()
        self.header.setStyleSheet("font-size: 24px; font-weight: 700;")

        self.idea_label = QLabel()
        self.idea_input = QTextEdit()
        self.idea_input.setFixedHeight(110)

        self.project_type_label = QLabel()
        self.project_type = QComboBox()
        self.project_type.addItems(PROJECT_TYPES)

        self.language_label = QLabel()
        self.language_select = QComboBox()
        self.language_select.addItem("العربية", "ar")
        self.language_select.addItem("English", "en")
        self.language_select.currentIndexChanged.connect(self.change_language)

        self.new_project_button = QPushButton()
        self.new_project_button.clicked.connect(self.new_project)

        self.save_project_button = QPushButton()
        self.save_project_button.clicked.connect(self.save_current_project)
        self.save_project_button.setEnabled(False)

        self.architecture_button = QPushButton()
        self.architecture_button.clicked.connect(self.generate_architecture)
        self.architecture_button.setEnabled(False)

        self.github_planner_button = QPushButton()
        self.github_planner_button.clicked.connect(self.generate_github_plan)
        self.github_planner_button.setEnabled(False)

        self.code_starter_button = QPushButton()
        self.code_starter_button.clicked.connect(self.generate_code_starter)
        self.code_starter_button.setEnabled(False)

        self.deployment_button = QPushButton()
        self.deployment_button.clicked.connect(
            self.generate_deployment_plan
        )
        self.deployment_button.setEnabled(False)

        self.open_project_button = QPushButton()
        self.open_project_button.clicked.connect(self.open_selected_project)
        self.architecture_button.setEnabled(True)
        self.github_planner_button.setEnabled(True)
        self.deployment_button.setEnabled(True)
        self.code_starter_button.setEnabled(True)
        

        self.refresh_projects_button = QPushButton()
        self.refresh_projects_button.clicked.connect(self.load_projects_list)

        self.delete_project_button = QPushButton()
        self.delete_project_button.clicked.connect(self.delete_selected_project)

        self.generate_button = QPushButton()
        self.generate_button.clicked.connect(self.generate_blueprint)

        self.export_button = QPushButton()
        self.export_button.clicked.connect(self.export_pdf)
        self.export_button.setEnabled(False)

        self.status_label = QLabel()

        self.projects_label = QLabel()
        self.projects_list = QListWidget()
        self.projects_list.setFixedWidth(330)
        self.projects_list.itemDoubleClicked.connect(self.open_selected_project)

        self.tabs = BlueprintTabs(language=self.language)

        controls = QHBoxLayout()
        controls.addWidget(self.project_type_label)
        controls.addWidget(self.project_type)
        controls.addWidget(self.language_label)
        controls.addWidget(self.language_select)
        controls.addWidget(self.new_project_button)
        controls.addWidget(self.save_project_button)
        controls.addWidget(self.generate_button)
        controls.addWidget(self.export_button)
        controls.addWidget(self.architecture_button)
        controls.addWidget(self.github_planner_button)
        controls.addWidget(self.deployment_button)
        controls.addWidget(self.code_starter_button)

        projects_buttons = QHBoxLayout()
        projects_buttons.addWidget(self.open_project_button)
        projects_buttons.addWidget(self.refresh_projects_button)
        projects_buttons.addWidget(self.delete_project_button)
        sidebar = QVBoxLayout()
        sidebar.addWidget(self.projects_label)
        sidebar.addWidget(self.projects_list)
        sidebar.addLayout(projects_buttons)

        main_content = QVBoxLayout()
        main_content.addWidget(self.header)
        main_content.addWidget(self.idea_label)
        main_content.addWidget(self.idea_input)
        main_content.addLayout(controls)
        main_content.addWidget(self.status_label)
        main_content.addWidget(self.tabs)

        self.footer_label = QLabel(
            "Foundry AI Beta v0.9 | Created by Abdullah Al Amri"
        )
        self.footer_label.setAlignment(Qt.AlignCenter)
        self.footer_label.setStyleSheet("""
            QLabel {
                color: #777777;
                font-size: 11px;
                padding: 6px;
            }
        """)

        main_content.addWidget(self.footer_label)

        root = QHBoxLayout()
        root.addLayout(sidebar)
        root.addLayout(main_content)

        container = QWidget()
        container.setLayout(root)
        self.setCentralWidget(container)

        self.apply_language()
        self.load_projects_list()

    def change_language(self) -> None:
        self.language = self.language_select.currentData()
        self.apply_language()

    def apply_language(self) -> None:
        is_ar = self.language == "ar"
        self.setLayoutDirection(Qt.RightToLeft if is_ar else Qt.LeftToRight)
        self.architecture_button.setText("بناء الهيكلة" if is_ar else "Build Architecture")
        self.header.setText(f"{t(self.language, 'headline')}\n{t(self.language, 'tagline')}")
        self.github_planner_button.setText("خطة GitHub" if is_ar else "GitHub Plan")
        self.deployment_button.setText("خطة النشر"if is_ar else "Deployment Plan")
        self.code_starter_button.setText("بدء البرمجة" if is_ar else "Start Code")
        self.header.setAlignment(Qt.AlignRight if is_ar else Qt.AlignLeft)
        
        self.idea_label.setText(t(self.language, "project_idea"))
        self.idea_input.setPlaceholderText(t(self.language, "idea_placeholder"))
        self.idea_input.setLayoutDirection(Qt.RightToLeft if is_ar else Qt.LeftToRight)
        self.idea_input.setAlignment(Qt.AlignRight if is_ar else Qt.AlignLeft)

        self.project_type_label.setText(t(self.language, "project_type"))
        self.language_label.setText(t(self.language, "language"))

        self.new_project_button.setText("مشروع جديد" if is_ar else "New Project")
        self.save_project_button.setText("حفظ المشروع" if is_ar else "Save Project")
        self.open_project_button.setText("فتح" if is_ar else "Open")
        self.refresh_projects_button.setText("تحديث" if is_ar else "Refresh")
        self.delete_project_button.setText("حذف" if is_ar else "Delete")
        self.projects_label.setText("المشاريع المحفوظة" if is_ar else "Saved Projects")
        self.architecture_button.setText("بناء الهيكلة" if is_ar else "Build Architecture")
        self.code_starter_button.setText("بدء البرمجة" if is_ar else "Start Code")

        self.generate_button.setText(t(self.language, "generate"))
        self.export_button.setText(t(self.language, "export_pdf"))
        self.status_label.setText(t(self.language, "ready"))
        self.tabs.set_language(self.language)

        self.load_projects_list()

    def load_projects_list(self) -> None:
        self.projects_list.clear()
        projects = self.project_manager.list_projects()

        for project in projects:
            idea = project.get("idea", "")
            project_type = project.get("project_type", "")
            created_at = project.get("created_at", "")
            project_id = project.get("id")

            title = idea[:45] + ("..." if len(idea) > 45 else "")
            item_text = f"#{project_id} | {project_type}\n{title}\n{created_at}"

            self.projects_list.addItem(item_text)

            item = self.projects_list.item(self.projects_list.count() - 1)
            item.setData(Qt.UserRole, project_id)

    def open_selected_project(self) -> None:
        selected = self.projects_list.currentItem()
        if not selected:
            QMessageBox.warning(
                self,
                "Foundry AI",
                "اختر مشروعًا من القائمة أولًا." if self.language == "ar" else "Select a project first.",
            )
            return

        project_id = selected.data(Qt.UserRole)
        project = self.project_manager.get_project(project_id)

        if not project:
            QMessageBox.critical(
                self,
                "Foundry AI",
                "لم يتم العثور على المشروع." if self.language == "ar" else "Project not found.",
            )
            return

        self.project_id = project["id"]
        self.blueprint = project["blueprint"]
        self.pending_idea = project["idea"]
        self.pending_project_type = project["project_type"]

        self.idea_input.setPlainText(project["idea"])
        self.project_type.setCurrentText(project["project_type"])
        self.tabs.set_blueprint(self.blueprint)

        self.export_button.setEnabled(True)
        self.save_project_button.setEnabled(True)
        self.architecture_button.setEnabled(True)
        self.github_planner_button.setEnabled(True)
        self.deployment_button.setEnabled(True)

        self.status_label.setText(
            "تم فتح المشروع." if self.language == "ar" else "Project opened."
        )

    def delete_selected_project(self) -> None:
        selected = self.projects_list.currentItem()

        if not selected:
            QMessageBox.warning(
                self,
                "Foundry AI",
                "اختر مشروعًا أولاً."
                if self.language == "ar"
                else "Select a project first."
            )
            return

        reply = QMessageBox.question(
            self,
            "Foundry AI",
            "هل تريد حذف المشروع نهائيًا؟"
            if self.language == "ar"
            else "Delete project permanently?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        project_id = selected.data(Qt.UserRole)

        self.project_manager.delete_project(project_id)

        if self.project_id == project_id:
            self.new_project()

        self.load_projects_list()

        self.status_label.setText(
            "تم حذف المشروع."
            if self.language == "ar"
            else "Project deleted."
        )
    def new_project(self) -> None:
        self.blueprint = None
        self.project_id = None
        self.pending_idea = ""
        self.pending_project_type = ""

        self.idea_input.clear()
        self.tabs.set_blueprint({})
        self.export_button.setEnabled(False)
        self.save_project_button.setEnabled(False)
        self.architecture_button.setEnabled(False)
        self.github_planner_button.setEnabled(False)
        self.deployment_button.setEnabled(False)
        self.code_starter_button.setEnabled(False)
        self.status_label.setText("تم إنشاء مشروع جديد." if self.language == "ar" else "New project created.")

    def save_current_project(self) -> None:
        if not self.blueprint:
            QMessageBox.warning(
                self,
                "Foundry AI",
                "لا يوجد مخطط لحفظه." if self.language == "ar" else "There is no blueprint to save.",
            )
            return

        idea = self.idea_input.toPlainText().strip() or self.pending_idea
        project_type = self.project_type.currentText() or self.pending_project_type

        self.project_id = self.project_manager.save_generated_project(
            idea,
            project_type,
            self.blueprint,
        )

        self.load_projects_list()

        QMessageBox.information(
            self,
            "Foundry AI",
            "تم حفظ المشروع بنجاح." if self.language == "ar" else "Project saved successfully.",
        )

    def generate_blueprint(self) -> None:
        try:
            idea = self.idea_input.toPlainText().strip()
            project_type = self.project_type.currentText()
            validate_project_idea(idea)

            self.pending_idea = idea
            self.pending_project_type = project_type

            self.generate_button.setEnabled(False)
            self.export_button.setEnabled(False)
            self.save_project_button.setEnabled(False)
            self.generate_button.setText(t(self.language, "generating"))

            self.status_label.setText("""
    🧠 Founder Agent      Running...
    📊 Market Agent       Running...
    🏗 Product Agent      Waiting...
    ⚙ Technical Agent    Waiting...
    🚀 Launch Agent       Waiting...
    """)

            self.thread = QThread()
            self.worker = BlueprintWorker(idea, project_type, self.language)
            self.worker.moveToThread(self.thread)

            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.on_generation_success)
            self.worker.failed.connect(self.on_generation_failed)
            self.worker.finished.connect(self.thread.quit)
            self.worker.failed.connect(self.thread.quit)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.finished.connect(self.cleanup_worker)
            self.thread.start()

        except Exception as exc:
            QMessageBox.critical(self, "Foundry AI", str(exc))
            self.reset_generation_buttons()
            
    def on_generation_success(self, blueprint: dict) -> None:
        self.blueprint = blueprint
        self.project_id = self.project_manager.save_generated_project(
            self.pending_idea,
            self.pending_project_type,
            self.blueprint,
        )

        self.load_projects_list()
        self.tabs.set_blueprint(self.blueprint)
        self.export_button.setEnabled(True)
        self.save_project_button.setEnabled(True)
        self.architecture_button.setEnabled(True)
        self.github_planner_button.setEnabled(True)
        self.deployment_button.setEnabled(True)
        self.code_starter_button.setEnabled(True)
        self.status_label.setText("""
🧠 Founder Agent      ✅ Complete
📊 Market Agent       ✅ Complete
🏗 Product Agent      ✅ Complete
⚙ Technical Agent    ✅ Complete
🚀 Launch Agent       ✅ Complete

🚀 Foundry Analysis Complete
""")
        self.reset_generation_buttons()

    @Slot(str)
    def on_generation_failed(self, error_message: str) -> None:
        self.status_label.setText(t(self.language, "status_failed"))
        QMessageBox.critical(self, "Foundry AI", error_message)
        self.reset_generation_buttons()

    @Slot()
    def cleanup_worker(self) -> None:
        self.worker = None
        self.thread = None

    def reset_generation_buttons(self) -> None:
        self.generate_button.setEnabled(True)
        self.generate_button.setText(t(self.language, "generate"))
    def generate_architecture(self) -> None:
        if not self.blueprint:
            QMessageBox.warning(
                self,
                "Foundry AI",
                "ولّد المخطط أولًا." if self.language == "ar" else "Generate the blueprint first.",
            )
            return

        self.architecture_button.setEnabled(False)
        self.status_label.setText(
            "جاري بناء الهيكلة التقنية..."
            if self.language == "ar"
            else "Building architecture..."
        )

        self.thread = QThread()
        self.worker = ArchitectureWorker(self.blueprint, self.language)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_architecture_success)
        self.worker.failed.connect(self.on_architecture_failed)

        self.worker.finished.connect(self.thread.quit)
        self.worker.failed.connect(self.thread.quit)

        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.cleanup_worker)

        self.thread.start()


    @Slot(dict)
    def on_architecture_success(self, architecture: dict) -> None:
        if "technical" not in self.blueprint:
            self.blueprint["technical"] = {}

        self.blueprint["technical"].update(architecture)

        self.tabs.set_blueprint(self.blueprint)

        self.architecture_button.setEnabled(True)

        self.status_label.setText(
            "تم بناء الهيكلة التقنية."
            if self.language == "ar"
            else "Architecture generated."
        )

    @Slot(str)
    def on_architecture_failed(self, error_message: str) -> None:
        self.architecture_button.setEnabled(True)

        self.status_label.setText(
            "فشل بناء الهيكلة."
            if self.language == "ar"
            else "Architecture generation failed."
        )

        QMessageBox.critical(
            self,
            "Foundry AI",
            error_message,
        )
    def generate_github_plan(self) -> None:
        if not self.blueprint:
            QMessageBox.warning(
                self,
                "Foundry AI",
                "ولّد المخطط أولًا." if self.language == "ar" else "Generate the blueprint first.",
            )
            return

        self.github_planner_button.setEnabled(False)
        self.status_label.setText(
            "جاري بناء خطة GitHub..."
            if self.language == "ar"
            else "Building GitHub plan..."
        )

        self.thread = QThread()
        self.worker = GitHubPlannerWorker(self.blueprint, self.language)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_github_plan_success)
        self.worker.failed.connect(self.on_github_plan_failed)

        self.worker.finished.connect(self.thread.quit)
        self.worker.failed.connect(self.thread.quit)

        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.cleanup_worker)

        self.thread.start()

    @Slot(dict)
    def on_github_plan_success(self, github_plan: dict) -> None:
        if "development" not in self.blueprint:
            self.blueprint["development"] = {}

        self.blueprint["development"].update(github_plan)

        self.tabs.set_blueprint(self.blueprint)
        self.github_planner_button.setEnabled(True)

        self.status_label.setText(
            "تم بناء خطة GitHub."
            if self.language == "ar"
            else "GitHub plan generated."
        )

    @Slot(str)
    def on_github_plan_failed(self, error_message: str) -> None:
        self.github_planner_button.setEnabled(True)

        self.status_label.setText(
            "فشل بناء خطة GitHub."
            if self.language == "ar"
            else "GitHub plan generation failed."
        )

        QMessageBox.critical(
            self,
            "Foundry AI",
            error_message,
        )
    def generate_deployment_plan(self) -> None:

        if not self.blueprint:
            return

        self.deployment_button.setEnabled(False)

        self.thread = QThread()

        self.worker = DeploymentAdvisorWorker(
            self.blueprint,
            self.language,
        )

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(
            self.worker.run
        )

        self.worker.finished.connect(
            self.on_deployment_success
        )

        self.worker.failed.connect(
            self.on_deployment_failed
        )

        self.worker.finished.connect(
            self.thread.quit
        )

        self.worker.failed.connect(
            self.thread.quit
        )

        self.thread.finished.connect(
            self.thread.deleteLater
        )

        self.thread.finished.connect(
            self.cleanup_worker
        )

        self.thread.start()


    @Slot(dict)
    def on_deployment_success(
        self,
        deployment: dict
    ) -> None:

        if "technical" not in self.blueprint:
            self.blueprint["technical"] = {}

        self.blueprint["technical"].update(
            deployment
        )

        self.tabs.set_blueprint(
            self.blueprint
        )

        self.deployment_button.setEnabled(True)

        self.status_label.setText(
            "تم إنشاء خطة النشر"
            if self.language == "ar"
            else "Deployment plan generated"
        )


    @Slot(str)
    def on_deployment_failed(
        self,
        error_message: str
    ) -> None:

        self.deployment_button.setEnabled(True)

        QMessageBox.critical(
            self,
            "Foundry AI",
            error_message,
        )
    def generate_code_starter(self) -> None:

        if not self.blueprint:
            return

        self.code_starter_button.setEnabled(False)

        self.thread = QThread()

        self.worker = CodeStarterWorker(
            self.blueprint,
            self.language,
        )

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(
            self.worker.run
        )

        self.worker.finished.connect(
            self.on_code_starter_success
        )

        self.worker.failed.connect(
            self.on_code_starter_failed
        )

        self.worker.finished.connect(
            self.thread.quit
        )

        self.worker.failed.connect(
            self.thread.quit
        )

        self.thread.finished.connect(
            self.thread.deleteLater
        )

        self.thread.finished.connect(
            self.cleanup_worker
        )

        self.thread.start()


    @Slot(dict)
    def on_code_starter_success(
        self,
        result: dict
    ) -> None:

        if "development" not in self.blueprint:
            self.blueprint["development"] = {}

        self.blueprint["development"].update(
            result
        )

        self.tabs.set_blueprint(
            self.blueprint
        )

        self.code_starter_button.setEnabled(True)

        self.status_label.setText(
            "تم إنشاء Code Starter"
            if self.language == "ar"
            else "Code Starter generated"
        )


    @Slot(str)
    def on_code_starter_failed(
        self,
        error_message: str
    ) -> None:

        self.code_starter_button.setEnabled(True)

        QMessageBox.critical(
            self,
            "Foundry AI",
            error_message,
        )
    def export_pdf(self) -> None:
            if not self.blueprint:
                return

            try:
                path = self.pdf_exporter.export(self.blueprint)
                QMessageBox.information(self, t(self.language, "export_complete"), f"PDF exported:\n{path}")
            except Exception as exc:
                QMessageBox.critical(self, t(self.language, "export_failed"), str(exc))