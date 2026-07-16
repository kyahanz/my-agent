from pathlib import Path

def read_file(filepath: str) -> str:
    try:
        path = Path(filepath)
        
        if not path.exists():
            return f"Error: File '{filepath}' tidak ditemukan."
        
        if not path.is_file():
            return f"Error: '{filepath}' bukan file."
        
        content = path.read_text(encoding="utf-8")
        return f"Isi file '{filepath}':\n\n{content}"
    
    except Exception as e:
        return f"Error baca file: {str(e)}"

def write_file(filepath: str, content: str) -> str:
    try:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return f"✅ File '{filepath}' berhasil ditulis."
    
    except Exception as e:
        return f"Error tulis file: {str(e)}"

def list_files(dirpath: str = ".") -> str:
    try:
        path = Path(dirpath)
        
        if not path.exists():
            return f"Error: Folder '{dirpath}' tidak ditemukan."
        
        files = []
        for item in sorted(path.iterdir()):
            if item.name.startswith('.') or item.name == 'venv':
                continue
            icon = "📁" if item.is_dir() else "📄"
            files.append(f"{icon} {item.name}")
        
        result = "\n".join(files)
        return f"Isi folder '{dirpath}':\n\n{result}"
    
    except Exception as e:
        return f"Error list files: {str(e)}"