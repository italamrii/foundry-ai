# Foundry AI

Foundry AI is a desktop AI co-founder and product builder that turns a raw project idea into a structured execution blueprint.

## V1 Features

- Enter a project idea
- Choose project type
- Generate a structured blueprint using OpenAI
- View blueprint sections in tabs
- Save generated projects locally in SQLite
- Export blueprint to PDF

## Setup

```bash
python -m venv .venv
.venv\\Scripts\\activate  # Windows
pip install -r requirements.txt
copy .env.example .env
```

Add your OpenAI API key to `.env`.

## Run

```bash
python main.py
```

## Notes

This is the first scalable skeleton. Upcoming improvements should include worker threads, section regeneration, project library, richer PDF styling, and markdown/docx export.
