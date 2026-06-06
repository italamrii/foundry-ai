import json
from typing import Any, Dict

from ai.openai_client import OpenAIClient


class ArchitectureBuilder:
    def __init__(self) -> None:
        self.ai_client = OpenAIClient()

    def generate(self, blueprint: Dict[str, Any], language: str = "ar") -> Dict[str, Any]:
        output_language = "Arabic" if language == "ar" else "English"

        schema = {
            "architecture_builder": {
                "recommended_stack": [],
                "database_schema": [],
                "api_endpoints": [],
                "folder_structure": [],
                "technical_decisions": [],
                "scalability_plan": []
            }
        }

        prompt = f"""
You are Foundry AI acting as a senior CTO and software architect.

Based on this project blueprint, generate a practical software architecture.

Output language: {output_language}

Rules:
- Return valid JSON only.
- No markdown.
- Keep JSON keys in English.
- Write values in {output_language}.
- Be practical and implementation-ready.
- Every list must contain at least 5 useful items.
- Focus on what a developer needs to start building.

Project Blueprint:
{json.dumps(blueprint, ensure_ascii=False, indent=2)}

Required JSON:
{json.dumps(schema, ensure_ascii=False, indent=2)}
"""

        return self.ai_client.generate_json(prompt)