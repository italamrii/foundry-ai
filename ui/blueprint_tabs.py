from typing import Any, Dict

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTabWidget, QTextEdit

from app.translations import TAB_LABELS, field_label


class BlueprintTabs(QTabWidget):
    TAB_KEYS = [
        "overview",
        "business",
        "product",
        "technical",
        "design",
        "development",
        "launch",
    ]

    def __init__(self, language: str = "en") -> None:
        super().__init__()
        self.language = language
        self.editors: dict[str, QTextEdit] = {}

        for key in self.TAB_KEYS:
            editor = QTextEdit()
            editor.setReadOnly(True)
            editor.setAcceptRichText(True)
            editor.setStyleSheet("""
                QTextEdit {
                    background-color: #141414;
                    border: 1px solid #2f2f2f;
                    border-radius: 10px;
                    padding: 14px;
                    color: #f5f5f5;
                }
            """)
            self._apply_editor_direction(editor)
            self.editors[key] = editor
            self.addTab(editor, TAB_LABELS[language][key])

    def set_language(self, language: str) -> None:
        self.language = language
        for index, key in enumerate(self.TAB_KEYS):
            self.setTabText(index, TAB_LABELS[language][key])
            self._apply_editor_direction(self.editors[key])

    def set_blueprint(self, blueprint: Dict[str, Any]) -> None:
        for key in self.TAB_KEYS:
            section = blueprint.get(key, {})
            title = TAB_LABELS[self.language][key]

            if key == "overview":
                html = self._render_overview_page(title, section)
            else:
                html = self._render_page(title, section)

            self.editors[key].setHtml(html)

    def _apply_editor_direction(self, editor: QTextEdit) -> None:
        editor.setLayoutDirection(Qt.RightToLeft if self.language == "ar" else Qt.LeftToRight)
        editor.setAlignment(Qt.AlignRight if self.language == "ar" else Qt.AlignLeft)

    def _base_html(self, title: str, content: str) -> str:
        direction = "rtl" if self.language == "ar" else "ltr"
        align = "right" if self.language == "ar" else "left"

        return f"""
        <html>
        <head>
        <style>
            body {{
                background: #141414;
                color: #f5f5f5;
                font-family: Tahoma, Arial, sans-serif;
                font-size: 15px;
                line-height: 1.7;
                text-align: {align};
            }}
            .page-title {{
                font-size: 25px;
                font-weight: 800;
                margin-bottom: 18px;
                padding-bottom: 10px;
                border-bottom: 1px solid #333;
            }}
            .hero {{
                background: #202020;
                border: 1px solid #343434;
                border-radius: 16px;
                padding: 22px;
                margin-bottom: 18px;
            }}
            .hero-title {{
                font-size: 26px;
                font-weight: 900;
                margin-bottom: 8px;
            }}
            .hero-subtitle {{
                font-size: 16px;
                color: #dddddd;
            }}
            .card {{
                background: #202020;
                border: 1px solid #343434;
                border-radius: 14px;
                padding: 14px;
                margin-bottom: 14px;
            }}
            .card-title {{
                font-size: 18px;
                font-weight: 800;
                color: #ffffff;
                margin-bottom: 8px;
            }}
            .summary-grid {{
                margin-top: 14px;
            }}
            .summary-item {{
                background: #1a1a1a;
                border: 1px solid #303030;
                border-radius: 12px;
                padding: 14px;
                margin-bottom: 12px;
            }}
            .summary-label {{
                font-size: 15px;
                font-weight: 800;
                margin-bottom: 6px;
                color: #ffffff;
            }}
            .summary-value {{
                font-size: 14px;
                color: #eeeeee;
            }}
            .score-card {{
                background: #181818;
                border: 1px solid #303030;
                border-radius: 12px;
                padding: 14px;
                margin-bottom: 10px;
            }}
            .score-label {{
                font-size: 14px;
                font-weight: 800;
                color: #ffffff;
                margin-bottom: 4px;
            }}
            .score-value {{
                font-size: 26px;
                font-weight: 900;
                color: #ffffff;
            }}
            .paragraph {{
                background: #181818;
                border-radius: 8px;
                padding: 10px;
                margin-top: 6px;
            }}
            ul {{
                margin-top: 6px;
                padding-right: 22px;
                padding-left: 22px;
            }}
            li {{
                margin-bottom: 8px;
                background: #181818;
                border-radius: 8px;
                padding: 9px;
            }}
            .empty {{
                padding: 55px;
                text-align: center;
                color: #999;
                font-size: 16px;
            }}
        </style>
        </head>
        <body dir="{direction}">
            <div class="page-title">{title}</div>
            {content}
        </body>
        </html>
        """

    def _render_overview_page(self, title: str, section: Any) -> str:
        if not section:
            empty = "لم يتم توليد هذا القسم بعد." if self.language == "ar" else "This section has not been generated yet."
            return self._base_html(title, f"<div class='empty'>{empty}</div>")

        if not isinstance(section, dict):
            return self._base_html(title, self._render_value(section))

        project_name = section.get("project_name", "Untitled Project")
        one_liner = section.get("one_liner", "")
        foundry_score = section.get("foundry_score", {})
        recommendations = section.get("founder_recommendations", [])

        score_html = ""
        if isinstance(foundry_score, dict):
            score_items = []

            for score_key in [
                "project_viability",
                "market_opportunity",
                "execution_complexity",
                "ai_confidence",
                "founder_fit",
                "speed_to_market",
                "revenue_potential",
                "defensibility",
            ]:
                if score_key in foundry_score:
                    score_items.append(f"""
                    <div class="score-card">
                        <div class="score-label">{field_label(self.language, score_key)}</div>
                        <div class="score-value">{foundry_score.get(score_key)} / 100</div>
                    </div>
                    """)

            reason = foundry_score.get("score_reason", "")
            if reason:
                score_items.append(f"""
                <div class="summary-item">
                    <div class="summary-label">{field_label(self.language, "score_reason")}</div>
                    <div class="summary-value">{reason}</div>
                </div>
                """)

            score_html = f"""
            <div class="card">
                <div class="card-title">{field_label(self.language, "foundry_score")}</div>
                {''.join(score_items)}
            </div>
            """

        recommendations_html = ""
        if isinstance(recommendations, list) and recommendations:
            rec_items = "".join(
                self._render_value(item)
                for item in recommendations
            )

            recommendations_html = f"""
            <div class="card">
                <div class="card-title">{field_label(self.language, "founder_recommendations")}</div>
                {rec_items}
            </div>
            """

        priority_keys = [
            "founder_verdict",
            "market_insights",
            "red_flags",
            "core_problem",
            "core_solution",
            "target_user",
            "positioning",
            "why_now",
            "success_definition",
        ]

        items = []
        for key in priority_keys:
            if key in section:
                value_html = self._render_value(section.get(key, ""), key)

                items.append(f"""
                <div class="summary-item">
                    <div class="summary-label">{field_label(self.language, key)}</div>
                    <div class="summary-value">{value_html}</div>
                </div>
                """)

        content = f"""
        <div class="hero">
            <div class="hero-title">{project_name}</div>
            <div class="hero-subtitle">{one_liner}</div>
        </div>

        {score_html}
        {recommendations_html}

        <div class="summary-grid">
            {''.join(items)}
        </div>
        """

        return self._base_html(title, content)

    def _render_page(self, title: str, section: Any) -> str:
        if not section:
            empty = "لم يتم توليد هذا القسم بعد." if self.language == "ar" else "This section has not been generated yet."
            content = f"<div class='empty'>{empty}</div>"
        else:
            content = self._render_value(section)

        return self._base_html(title, content)

    def _render_value(self, value: Any, key: str | None = None) -> str:
        if isinstance(value, dict):
            if all(
                k in value
                for k in ["recommendation", "reasoning", "concrete_action", "what_to_avoid"]
            ):
                return f"""
                <div class="card">
                    <div class="card-title">التوصية</div>
                    <div class="paragraph"><b>التوصية:</b><br>{value.get("recommendation", "")}</div>
                    <div class="paragraph"><b>سبب التوصية:</b><br>{value.get("reasoning", "")}</div>
                    <div class="paragraph"><b>الإجراء العملي:</b><br>{value.get("concrete_action", "")}</div>
                    <div class="paragraph"><b>ما يجب تجنبه:</b><br>{value.get("what_to_avoid", "")}</div>
                </div>
                """

            if all(
                k in value
                for k in ["risk", "why_it_matters", "how_to_reduce_it"]
            ):
                return f"""
                <div class="card">
                    <div class="card-title">مؤشر خطر</div>
                    <div class="paragraph"><b>الخطر:</b><br>{value.get("risk", "")}</div>
                    <div class="paragraph"><b>لماذا يهم؟</b><br>{value.get("why_it_matters", "")}</div>
                    <div class="paragraph"><b>كيف تقلل الخطر؟</b><br>{value.get("how_to_reduce_it", "")}</div>
                </div>
                """

            html = []
            for child_key, child_value in value.items():
                title = field_label(self.language, child_key)
                html.append(f"""
                <div class="card">
                    <div class="card-title">{title}</div>
                    {self._render_value(child_value, child_key)}
                </div>
                """)
            return "\n".join(html)

        if isinstance(value, list):
            if not value:
                return "<div class='paragraph'>—</div>"

            if all(isinstance(item, dict) for item in value):
                return "".join(
                    self._render_value(item)
                    for item in value
                )

            items = []
            for item in value:
                items.append(f"<li>{self._render_value(item).strip()}</li>")

            return f"<ul>{''.join(items)}</ul>"

        if value is None or value == "":
            return "<div class='paragraph'>—</div>"

        return f"<div class='paragraph'>{value}</div>"