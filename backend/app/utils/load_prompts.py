import os

def load_prompt(folder: str, file_name: str) -> str:
    """Loads a prompt from a specific folder inside the app/prompts directory."""
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", folder, file_name)

    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    with open(prompt_path, "r", encoding="utf-8") as file:
        return file.read().strip()
