import json
from typing import Any, Dict
from data.database import get_connection


class ProjectRepository:
    def create_project(self, name: str, idea: str, project_type: str) -> int:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO projects (name, idea, project_type, status) VALUES (?, ?, ?, ?)",
                (name, idea, project_type, "generated"),
            )
            conn.commit()
            return int(cursor.lastrowid)

    def save_blueprint(self, project_id: int, blueprint: Dict[str, Any]) -> int:
        with get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO blueprints (
                    project_id,
                    business_json,
                    product_json,
                    technical_json,
                    design_json,
                    development_json,
                    launch_json,
                    full_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    project_id,
                    json.dumps(blueprint.get("business", {}), ensure_ascii=False),
                    json.dumps(blueprint.get("product", {}), ensure_ascii=False),
                    json.dumps(blueprint.get("technical", {}), ensure_ascii=False),
                    json.dumps(blueprint.get("design", {}), ensure_ascii=False),
                    json.dumps(blueprint.get("development", {}), ensure_ascii=False),
                    json.dumps(blueprint.get("launch", {}), ensure_ascii=False),
                    json.dumps(blueprint, ensure_ascii=False),
                ),
            )
            conn.commit()
            return int(cursor.lastrowid)
