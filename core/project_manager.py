import json
from typing import Any, Dict, List, Optional

from data.database import init_db, get_connection


class ProjectManager:
    def __init__(self) -> None:
        init_db()

    def save_generated_project(self, idea: str, project_type: str, blueprint: Dict[str, Any]) -> int:
        project_name = blueprint.get("overview", {}).get("project_name", "Untitled Project")

        with get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO projects (name, idea, project_type, status)
                VALUES (?, ?, ?, ?)
                """,
                (project_name, idea, project_type, "generated"),
            )
            project_id = int(cursor.lastrowid)

            conn.execute(
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
            return project_id

    def list_projects(self) -> List[Dict[str, Any]]:
        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT id, name, idea, project_type, created_at
                FROM projects
                ORDER BY id DESC
                """
            ).fetchall()

        return [dict(row) for row in rows]

    def get_project(self, project_id: int) -> Optional[Dict[str, Any]]:
        with get_connection() as conn:
            row = conn.execute(
                """
                SELECT 
                    p.id,
                    p.name,
                    p.idea,
                    p.project_type,
                    p.created_at,
                    b.full_json
                FROM projects p
                JOIN blueprints b ON b.project_id = p.id
                WHERE p.id = ?
                ORDER BY b.id DESC
                LIMIT 1
                """,
                (project_id,),
            ).fetchone()

        if not row:
            return None

        project = dict(row)
        project["blueprint"] = json.loads(project["full_json"])
        return project
    
    def delete_project(self, project_id: int) -> None:
        with get_connection() as conn:
            conn.execute(
                "DELETE FROM blueprints WHERE project_id = ?",
                (project_id,),
            )

            conn.execute(
                "DELETE FROM projects WHERE id = ?",
                (project_id,),
            )

            conn.commit()