from agent.loop import chat, conversation_history
from memory.long_term import init_db, load_history, clear_history


def main():
    init_db()

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