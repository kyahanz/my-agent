import httpx
import json
from tools.file_tool import read_file, write_file, list_files
from tools.bash_tool import run_bash
from memory.long_term import init_db, save_message, load_history, clear_history

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5-coder:3b"
# MODEL = "qwen2.5-coder:7b"

conversation_history = []

SYSTEM_PROMPT = """Kamu adalah AI coding assistant yang helpful.
Kamu berjalan di sistem operasi WINDOWS. Gunakan command Windows (bukan Linux).
Contoh: gunakan 'python hello.py' bukan './hello.py', gunakan 'dir' bukan 'ls'.

Kamu punya akses ke tools berikut. Kalau butuh pake tool, balas HANYA dengan format JSON ini:
{
    "tool": "nama_tool",
    "params": {"param1": "value1"}
}

Tools yang tersedia:
- read_file: baca isi file. params: {"filepath": "path/ke/file"}
- write_file: tulis file. params: {"filepath": "path/file", "content": "isinya"}
- list_files: lihat isi folder. params: {"dirpath": "."}
- run_bash: jalankan command terminal. params: {"command": "perintahnya"}

Kalau tidak butuh tool, jawab langsung seperti biasa dalam Bahasa Indonesia."""


def parse_tool_call(response: str):
    try:
        response = response.strip()

        if "```" in response:
            lines = response.split("\n")
            cleaned = []
            for line in lines:
                if line.strip().startswith("```"):
                    continue
                cleaned.append(line)
            response = "\n".join(cleaned).strip()

        if response.startswith("{"):
            data = json.loads(response)
            if "tool" in data and "params" in data:
                return data
    except:
        pass
    return None


def execute_tool(tool_name: str, params: dict) -> str:
    print(f"🔧 Menjalankan tool: {tool_name} dengan params: {params}")

    if tool_name == "read_file":
        return read_file(params.get("filepath", ""))
    elif tool_name == "write_file":
        return write_file(params.get("filepath", ""), params.get("content", ""))
    elif tool_name == "list_files":
        return list_files(params.get("dirpath", "."))
    elif tool_name == "run_bash":
        return run_bash(params.get("command", ""))
    else:
        return f"Error: tool '{tool_name}' tidak dikenal."


def chat(user_message: str) -> str:
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    save_message("user", user_message)

    while True:
        response = httpx.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *conversation_history
                ],
                "stream": False
            },
            timeout=300
        )

        data = response.json()
        assistant_message = data["message"]["content"]
        tool_call = parse_tool_call(assistant_message)

        if tool_call:
            tool_result = execute_tool(tool_call["tool"], tool_call["params"])
            print(f"📄 Hasil tool: {tool_result[:100]}...")
            conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            conversation_history.append({
                "role": "user",
                "content": f"Hasil tool '{tool_call['tool']}':\n{tool_result}"
            })
        else:
            conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            save_message("assistant", assistant_message)
            return assistant_message


def main():
    init_db()
    
    # Load history dari database
    past_history = load_history(limit=10)
    if past_history:
        conversation_history.extend(past_history)
        print(f"📚 Loaded {len(past_history)} pesan dari memory sebelumnya.\n")

    print("🤖 Agent lo siap! Ketik 'exit' untuk keluar.\n")
    print("Commands khusus: 'history', 'clear memory'\n")

    while True:
        user_input = input("Lo: ")

        if user_input.lower() == "exit":
            print("Agent: Dadah bro!")
            break
        elif user_input.lower() == "history":
            history = load_history()
            print(f"\n📚 {len(history)} pesan tersimpan di memory.\n")
            continue
        elif user_input.lower() == "clear memory":
            print(clear_history())
            conversation_history.clear()
            continue

        if not user_input.strip():
            continue

        print("Agent: (lagi mikir...)")
        response = chat(user_input)
        print(f"Agent: {response}\n")


if __name__ == "__main__":
    main()