"""Non-interactive demo: runs sample questions through DevBot."""
from chatbot import DevBot

QUESTIONS = [
    "hello",
    "what projects have you built?",
    "give me a python tip",
    "what is machine learning?",
    "who is deven?",
    "tell me a joke about quantum physics",
]

if __name__ == "__main__":
    bot = DevBot()
    for q in QUESTIONS:
        print(f"You:    {q}")
        print(f"DevBot: {bot.reply(q)}\n")
