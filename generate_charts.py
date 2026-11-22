"""
Generate the README result chart for DevBot.

Asks the bot's matcher a set of sample questions, records the best
cosine-similarity score for each, and saves a bar chart showing
which questions pass the 0.3 answer threshold to assets/result.png.

Run:  python generate_charts.py
"""

import tempfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

from chatbot import THRESHOLD, DevBot

NAVY = "#0B3C5D"
GOLD = "#E3A82B"
CREAM = "#F7F1E1"
GREY = "#9CA3AF"
OUT = Path(__file__).parent / "assets" / "result.png"

# (question, short label for the chart)
QUESTIONS = [
    ("hello", "hello"),
    ("what projects have you built?", "your projects?"),
    ("give me a python tip", "python tip"),
    ("what is machine learning?", "what is ML?"),
    ("who is deven?", "who is Deven?"),
    ("tell me a joke about quantum physics", "quantum joke\n(off-topic)"),
]


def best_score(bot: DevBot, message: str):
    """Return (best similarity score, matched tag) for one message."""
    vec = bot.vectorizer.transform([message.lower()])
    scores = cosine_similarity(vec, bot.matrix)[0]
    best = scores.argmax()
    return float(scores[best]), bot.tags[best]


def main() -> None:
    # Log goes to a temp file so chart runs never pollute the real log.
    bot = DevBot(
        intents_path=str(Path(__file__).parent / "intents.json"),
        log_path=str(Path(tempfile.gettempdir()) / "devbot_chart_log.txt"),
    )
    labels, scores, colours = [], [], []
    for question, label in QUESTIONS:
        score, tag = best_score(bot, question)
        matched = tag if score >= THRESHOLD else "fallback"
        print(f"{question!r}: score {score:.2f} -> {matched}")
        labels.append(label)
        scores.append(score)
        colours.append(NAVY if score >= THRESHOLD else GREY)

    fig, ax = plt.subplots(figsize=(9, 4.6))
    fig.patch.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)
    bars = ax.bar(labels, scores, color=colours, width=0.55)
    for bar, score in zip(bars, scores):
        ax.text(bar.get_x() + bar.get_width() / 2, score + 0.02,
                f"{score:.2f}", ha="center", fontweight="bold")
    ax.axhline(THRESHOLD, color=GOLD, linestyle="--", linewidth=2,
               label=f"Answer threshold ({THRESHOLD}) — below it, DevBot says it doesn't know")
    ax.set_ylim(0, 1.12)
    ax.set_ylabel("Best match score (cosine similarity)")
    ax.set_title("DevBot — match confidence per question (6 intents, 24 patterns)",
                 fontsize=12, fontweight="bold", color=NAVY)
    ax.legend(loc="upper right", fontsize=8)
    ax.tick_params(axis="x", labelsize=8)
    plt.tight_layout()
    OUT.parent.mkdir(exist_ok=True)
    plt.savefig(OUT, dpi=150)
    print(f"Chart saved to {OUT}")


if __name__ == "__main__":
    main()
