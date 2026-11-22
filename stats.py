"""
DevBot knowledge stats.

Counts what the bot knows: how many intents (topics), example
questions (patterns) and possible replies live in intents.json.

Run:  python stats.py
"""

import json
from pathlib import Path


def count_stats(intents_path: str = "intents.json") -> dict:
    """Return counts of intents, patterns and responses."""
    data = json.loads(Path(intents_path).read_text())
    intents = data["intents"]
    return {
        "intents": len(intents),
        "patterns": sum(len(i["patterns"]) for i in intents),
        "responses": sum(len(i["responses"]) for i in intents),
        "per_intent": {i["tag"]: len(i["patterns"]) for i in intents},
    }


def main() -> None:
    stats = count_stats()
    print(f"Intents (topics) : {stats['intents']}")
    print(f"Example patterns : {stats['patterns']}")
    print(f"Possible replies : {stats['responses']}")
    print("\nPatterns per intent:")
    for tag, count in stats["per_intent"].items():
        print(f"  {tag:<14} {count}")


if __name__ == "__main__":
    main()
