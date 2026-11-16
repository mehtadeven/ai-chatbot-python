"""
DevBot - a small AI chatbot
---------------------------
How it works (no heavy frameworks, just scikit-learn):
1. intents.json holds example phrases ("patterns") for each topic ("tag")
2. TF-IDF turns every pattern into a numeric vector
3. Your message is vectorised the same way, and cosine similarity finds
   the closest pattern - that topic's response is the reply
4. Questions the bot cannot answer are saved to unknown_questions.txt,
   so the owner can see what to teach it next

Run:  python chatbot.py
Type 'bye' to exit.
"""

import json
import random
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

THRESHOLD = 0.3  # below this similarity, the bot admits it does not know


class DevBot:
    def __init__(self, intents_path: str = "intents.json",
                 log_path: str = "unknown_questions.txt") -> None:
        data = json.loads(Path(intents_path).read_text())
        self.intents = data["intents"]
        self.fallback = data["fallback"]
        self.log_path = Path(log_path)  # where unanswered questions are saved
        self.patterns, self.tags = [], []
        for intent in self.intents:
            for pattern in intent["patterns"]:
                self.patterns.append(pattern)
                self.tags.append(intent["tag"])
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform(self.patterns)

    def log_unknown(self, message: str) -> None:
        # save one unanswered question per line, so it can be taught later
        with self.log_path.open("a", encoding="utf-8") as log_file:
            log_file.write(message.strip() + "\n")

    def reply(self, message: str) -> str:
        vec = self.vectorizer.transform([message.lower()])
        scores = cosine_similarity(vec, self.matrix)[0]
        best = scores.argmax()
        if scores[best] < THRESHOLD:
            self.log_unknown(message)  # remember what the bot could not answer
            return self.fallback
        tag = self.tags[best]
        intent = next(i for i in self.intents if i["tag"] == tag)
        return random.choice(intent["responses"])


def main() -> None:
    bot = DevBot()
    print("DevBot: Hello! I'm DevBot. Ask me about Python, ML, or Deven's projects. (type 'bye' to exit)")
    while True:
        try:
            user = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nDevBot: Bye! Keep building.")
            break
        if not user:
            continue
        print(f"DevBot: {bot.reply(user)}")
        if user.lower() in {"bye", "goodbye", "exit"}:
            break


if __name__ == "__main__":
    main()
