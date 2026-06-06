import json
from typing import Any, Dict
from openai import OpenAI
from app.config import OPENAI_API_KEY, OPENAI_MODEL
from ai.prompts.system_prompt import FOUNDRY_SYSTEM_PROMPT


class OpenAIClient:
    def __init__(self) -> None:
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is missing. Create a .env file from .env.example.")
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate_json(self, prompt: str) -> Dict[str, Any]:
        response = self.client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": FOUNDRY_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content or "{}"
        return json.loads(content)
