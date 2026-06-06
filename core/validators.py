def validate_project_idea(idea: str) -> None:
    if not idea or len(idea.strip()) < 10:
        raise ValueError("Please enter a clearer project idea with at least 10 characters.")
