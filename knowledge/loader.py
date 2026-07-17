from pathlib import Path

KNOWLEDGE_DIR = Path("knowledge")

def load_knowledge() -> str:
    knowledge_text = ""
    
    for file in KNOWLEDGE_DIR.glob("*.md"):
        content = file.read_text(encoding="utf-8")
        knowledge_text += f"\n\n## From {file.name}:\n{content}"
    
    return knowledge_text.strip()