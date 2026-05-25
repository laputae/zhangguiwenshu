from pathlib import Path


def load_prompt(name: str):
    prompt_path = Path(__file__).parent[2] / 'prompts' / f"{name}.prompt"
    return prompt_path.read_text(encoding="utf-8")
