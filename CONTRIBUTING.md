# Contributing to DevBot

Thanks for your interest! DevBot is a small learning project, so the rules
are simple: keep the code easy to read, and test before you send a change.

## Setup

```bash
git clone https://github.com/mehtadeven/ai-chatbot-python.git
cd ai-chatbot-python
pip install -r requirements.txt
```

## Run it

```bash
python chatbot.py   # interactive chat (type 'bye' to exit)
python demo.py      # scripted demonstration
```

## Run the tests

```bash
pip install pytest
python -m pytest
```

All tests should pass before you open a pull request.

## Add a new intent (teach the bot a new topic)

The bot's knowledge lives in `intents.json` — no code changes needed.
Add one object to the `intents` list:

```json
{"tag": "hobbies",
 "patterns": ["what are your hobbies", "do you have hobbies"],
 "responses": ["I enjoy reading about new ML models and helping with Python."]}
```

- `tag` — a short, unique name for the topic (lowercase, underscores ok)
- `patterns` — example ways a user might ask; add several phrasings
- `responses` — one or more replies; the bot picks one at random

Tip: check `unknown_questions.txt` after running the bot — it lists real
questions the bot could not answer, which is the best guide for what
intent to add next.

## Suggest a change

- **Found a bug or have an idea?** Open an issue describing what happened
  (or what you expected) and the question you typed.
- **Want to fix it yourself?** Fork the repo, make your change on a new
  branch, run the tests, and open a pull request explaining the change
  in one or two lines.

## Code style

- Simple, clearly named code with short comments — a beginner should be
  able to read `chatbot.py` top to bottom and explain how it works.
- No API keys, passwords, or personal data in code or commits.
