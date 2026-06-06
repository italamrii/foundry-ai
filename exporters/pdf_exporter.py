from pathlib import Path
from typing import Any, Dict
from fpdf import FPDF
from app.config import STORAGE_DIR


class PDFExporter:
    def export(self, blueprint: Dict[str, Any]) -> str:
        project_name = blueprint.get("overview", {}).get("project_name", "foundry_blueprint")
        safe_name = "".join(ch for ch in project_name if ch.isalnum() or ch in (" ", "-", "_")).strip().replace(" ", "_")
        output_path = STORAGE_DIR / f"{safe_name or 'foundry_blueprint'}.pdf"

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 20)
        pdf.multi_cell(0, 10, "Foundry AI Blueprint")
        pdf.ln(4)

        pdf.set_font("Helvetica", "", 12)
        self._write_value(pdf, blueprint)
        pdf.output(str(output_path))
        return str(output_path)

    def _write_value(self, pdf: FPDF, value: Any, level: int = 0) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                title = key.replace("_", " ").title()
                pdf.set_font("Helvetica", "B", max(12, 16 - level))
                pdf.multi_cell(0, 8, f"{'  ' * level}{title}")
                pdf.set_font("Helvetica", "", 11)
                self._write_value(pdf, child, level + 1)
                pdf.ln(1)
        elif isinstance(value, list):
            for item in value:
                text = self._stringify(item)
                pdf.multi_cell(0, 7, f"{'  ' * level}- {text}")
        else:
            pdf.multi_cell(0, 7, f"{'  ' * level}{self._stringify(value)}")

    def _stringify(self, value: Any) -> str:
        if isinstance(value, dict):
            return "; ".join(f"{k}: {v}" for k, v in value.items())
        return str(value)
