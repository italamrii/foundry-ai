import json

from ai.openai_client import OpenAIClient


class CodeStarter:
    def __init__(self):
        self.ai_client = OpenAIClient()

    def generate(self, blueprint, language="ar"):
        output_language = "Arabic" if language == "ar" else "English"

        schema = {
            "code_starter": {
                "project_structure": [],
                "development_tasks": [],
                "github_issues": [],
                "ai_coding_prompts": [],
                "acceptance_criteria": []
            }
        }

        prompt = f"""
You are Foundry AI acting as a senior CTO and technical lead.

Generate a developer-ready build package.

Output language:
{output_language}

Rules:
- Return valid JSON only.
- No markdown.
- Keep JSON keys in English.
- Write values in {output_language}.
- Be practical and implementation-ready.
- Do not generate full application code yet.
- Generate clear coding prompts that a developer can use in Cursor, Claude, GitHub Copilot, or ChatGPT.
- Focus on the first MVP sprint.

Project Blueprint:
{json.dumps(blueprint, ensure_ascii=False, indent=2)}

Required JSON:
{json.dumps(schema, ensure_ascii=False, indent=2)}
"""

        return self.ai_client.generate_json(prompt)