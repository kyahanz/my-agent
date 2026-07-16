import subprocess

def run_bash(command: str) -> str:
    try:
        print(f"💻 Menjalankan command: {command}")
        
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = ""
        
        if result.stdout:
            output += f"Output:\n{result.stdout}"
        
        if result.stderr:
            output += f"\nError:\n{result.stderr}"
        
        if not output:
            output = "Command selesai tanpa output."
            
        return output
    
    except subprocess.TimeoutExpired:
        return "Error: Command timeout (lebih dari 30 detik)."
    
    except Exception as e:
        return f"Error: {str(e)}"