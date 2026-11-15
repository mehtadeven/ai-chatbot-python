# 🤖 DevBot — AI Chatbot in Python


![Banner](assets/banner.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue) ![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange) ![Status](https://img.shields.io/badge/status-working-brightgreen)

A small chatbot that actually *understands* what you mean — not with if-else rules, but with **TF-IDF + cosine similarity** intent matching, the same idea behind real customer-support bots.

## 💬 Demo

```
You:    what projects have you built?
DevBot: Deven has built: a Digit Recognizer (98.9% accuracy), a Spam SMS
        Classifier, a Movie Recommender, this chatbot, and a Text Summarizer.

You:    what is machine learning?
DevBot: Machine Learning is teaching computers to find patterns in data
        instead of hand-writing every rule...

You:    tell me a joke about quantum physics
DevBot: I didn't quite get that. Try asking about Deven's projects...
```

That last one matters: when no intent is similar enough, DevBot honestly says so instead of guessing — a real design decision, not a bug.

## ⚙️ How it works

1. `intents.json` holds example phrases for each topic (greetings, projects, Python tips, ML questions…)
2. TF-IDF converts every phrase into a numeric vector (common words like "tell me" are ignored)
3. Your message is vectorised the same way; **cosine similarity** finds the closest intent
4. If the best match is too weak (below 0.3), the fallback reply is used

## 🚀 Run it

```bash
pip install -r requirements.txt
python chatbot.py   # interactive chat
python demo.py      # scripted demo questions
```

Add your own topics by editing `intents.json` — no code changes needed.

## 🧠 What I learned

- Intent classification: how chatbots map free text to actions
- Why stop-words and similarity thresholds matter (my first version confidently answered a quantum-physics joke with Deven's bio — the threshold + stop-words fixed it)
- Designing honest fallbacks instead of confident nonsense

## 🔮 Next steps

- [ ] Train a Logistic Regression classifier on the intents
- [ ] Add a Streamlit web UI
- [ ] Connect a real LLM API for open-ended questions

---
Built by [Mehta Deven](https://github.com/mehtadeven) — IT student learning ML/AI in public.
