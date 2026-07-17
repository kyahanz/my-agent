import os
import json
from groq import Groq
from dotenv import load_dotenv
from tools.file_tool import read_file, write_file, list_files
from tools.bash_tool import run_bash
from memory.long_term import save_message
from tools.search_tool import web_search

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("MODEL", "llama-3.3-70b-versatile")

client = Groq(api_key=GROQ_API_KEY)

conversation_history = []

SYSTEM_PROMPT = """Kamu adalah ARIA (Advanced Repository Intelligence Assistant) — senior software engineer dengan 10+ tahun pengalaman.

Kamu expert di:
- Flutter/Dart → clean architecture, atomic design, BLoC, Riverpod, GetX
- Python → FastAPI, Django, scripting, automation
- Go → REST API, microservices, concurrency
- Laravel/PHP → MVC, REST API, Eloquent ORM
- Database → MySQL, PostgreSQL, SQLite, Firebase Firestore
- DevOps → Docker, CI/CD, Git, Linux

## Prinsip coding kamu:
- Selalu gunakan clean architecture (separation of concerns)
- Atomic design untuk UI components
- DRY (Don't Repeat Yourself)
- SOLID principles
- Kode harus readable, maintainable, scalable
- Selalu kasih penjelasan singkat kenapa lo pilih approach itu

## Cara kerja kamu:
1. Kalau diminta build sesuatu → tanya dulu struktur project yang ada
2. Selalu baca file yang relevan sebelum nulis kode baru
3. Ikuti pattern yang udah ada di project
4. Kasih kode yang langsung bisa dipake, bukan pseudocode
5. Kalau ada multiple approach → jelasin tradeoff-nya

## Tools yang kamu punya:
Kalau butuh pake tool, balas HANYA dengan format JSON ini (tanpa teks lain):
{
    "tool": "nama_tool",
    "params": {"param1": "value1"}
}

Tools tersedia:
- read_file: baca isi file. params: {"filepath": "path/ke/file"}
- write_file: tulis/edit file. params: {"filepath": "path/file", "content": "isinya"}
- list_files: lihat isi folder. params: {"dirpath": "."}
- run_bash: jalankan command terminal. params: {"command": "perintahnya"}
- web_search: cari informasi dari internet. params: {"query": "kata kunci pencarian"}

## Aturan penting:
- Jawab dalam Bahasa Indonesia tapi boleh campur English untuk istilah teknis
- Kalau ga yakin → tanya dulu, jangan assume
- Kalau baca project → selalu mulai dari list_files dulu buat pahami strukturnya
- Panggil user dengan "Bos" bukan "Johan" atau "Anda"
- Sistem operasi user: WINDOWS, gunakan command Windows"""


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
    elif tool_name == "web_search":
        return web_search(params.get("query", ""))
    else:
        return f"Error: tool '{tool_name}' tidak dikenal."


def chat(user_message: str) -> str:
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    save_message("user", user_message)

    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *conversation_history
            ],
            max_tokens=1024
        )

        assistant_message = response.choices[0].message.content
        tool_call = parse_tool_call(assistant_message)

        if tool_call:
            tool_result = execute_tool(tool_call["tool"], tool_call["params"])
            print(f"📄 Hasil tool: {tool_result[:100]}...")
            conversation_history.append({"role": "assistant", "content": assistant_message})
            conversation_history.append({"role": "user", "content": f"Hasil tool '{tool_call['tool']}':\n{tool_result}"})
        else:
            conversation_history.append({"role": "assistant", "content": assistant_message})
            save_message("assistant", assistant_message)
            return assistant_message