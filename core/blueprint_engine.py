from typing import Any, Dict
from ai.openai_client import OpenAIClient
from core.prompt_builder import build_blueprint_prompt


class BlueprintEngine:
    def __init__(self) -> None:
        self.ai_client = OpenAIClient()

    def generate(self, idea: str, project_type: str, language: str = "en") -> Dict[str, Any]:
        prompt = build_blueprint_prompt(idea=idea, project_type=project_type, language=language)
        return self.ai_client.generate_json(prompt)
