import json
from typing import Any, Dict

from ai.openai_client import OpenAIClient


class DeploymentAdvisor:
    def __init__(self) -> None:
        self.ai_client = OpenAIClient()

    def generate(self, blueprint: Dict[str, Any], language: str = "ar") -> Dict[str, Any]:
        output_language = "Arabic" if language == "ar" else "English"

        schema = {
            "deployment_advisor": {
                "recommended_hosting": [],
                "deployment_architecture": [],
                "monthly_cost_estimate": [],
                "scaling_strategy": [],
                "devops_checklist": []
            }
        }

        prompt = f"""
You are Foundry AI acting as a senior DevOps Architect.

Output language: {output_language}

Rules:
- Return valid JSON only.
- No markdown.
- Keep JSON keys in English.
- Write values in {output_language}.
- Every list must contain at least 5 useful items.

Project Blueprint:
{json.dumps(blueprint, ensure_ascii=False, indent=2)}

Required JSON:
{json.dumps(schema, ensure_ascii=False, indent=2)}
"""

        return self.ai_client.generate_json(prompt)