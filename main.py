import httpx
import json

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5-coder:7b"

conversation_history = []

def chat(user_message):
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    response = httpx.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": conversation_history,
            "stream": False
        },
        timeout=120
    )
    
    data = response.json()
    assistant_message = data["message"]["content"]
    
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })
    
    return assistant_message

def main():
    print("🤖 Agent lo siap! Ketik 'exit' untuk keluar.\n")
    
    while True:
        user_input = input("Lo: ")
        
        if user_input.lower() == "exit":
            print("Agent: Dadah bro!")
            break
            
        if not user_input.strip():
            continue
        
        print("Agent: (lagi mikir...)")
        response = chat(user_input)
        print(f"Agent: {response}\n")

if __name__ == "__main__":
    main()