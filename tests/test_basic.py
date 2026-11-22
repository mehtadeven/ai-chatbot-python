"""Basic tests for DevBot.

Run from the project folder:  python -m pytest
"""

import json
import sys
from pathlib import Path

import pytest

# make chatbot.py importable when pytest runs from the project root
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from chatbot import DevBot  # noqa: E402

INTENTS_PATH = PROJECT_ROOT / "intents.json"


@pytest.fixture()
def bot(tmp_path):
    # log goes to a temp folder, so tests never touch the real log file
    return DevBot(intents_path=str(INTENTS_PATH),
                  log_path=str(tmp_path / "unknown_questions.txt"))


def load_intents():
    return json.loads(INTENTS_PATH.read_text())


def test_greeting_gets_a_greeting_reply(bot):
    greeting = next(i for i in load_intents()["intents"] if i["tag"] == "greeting")
    assert bot.reply("hello") in greeting["responses"]


def test_off_topic_question_gets_the_fallback(bot):
    answer = bot.reply("tell me a joke about quantum physics")
    assert answer == load_intents()["fallback"]


def test_unknown_question_is_logged(bot, tmp_path):
    question = "what is the weather like on mars"
    bot.reply(question)
    logged = (tmp_path / "unknown_questions.txt").read_text()
    assert question in logged


def test_known_question_is_not_logged(bot, tmp_path):
    bot.reply("hello")
    log_file = tmp_path / "unknown_questions.txt"
    assert not log_file.exists() or log_file.read_text() == ""


def test_stats_count_the_bots_knowledge():
    from stats import count_stats

    stats = count_stats(str(INTENTS_PATH))
    data = load_intents()
    assert stats["intents"] == len(data["intents"])
    assert stats["patterns"] == sum(len(i["patterns"]) for i in data["intents"])
    assert stats["responses"] >= stats["intents"]


def test_every_intent_has_patterns_and_responses():
    data = load_intents()
    assert data["intents"], "intents list is empty"
    for intent in data["intents"]:
        assert intent["tag"], "intent is missing a tag"
        assert intent["patterns"], f"{intent['tag']} has no patterns"
        assert intent["responses"], f"{intent['tag']} has no responses"
    assert data["fallback"], "fallback message is missing"
