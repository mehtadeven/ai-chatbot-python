// DevBot - browser version of chatbot.py.
// TF-IDF turns every example pattern in intents.json into a vector; your
// message is vectorised the same way and cosine similarity picks the closest
// pattern. Below THRESHOLD the bot says it doesn't know instead of guessing.

const STOPS = new Set(SKLEARN_STOP_WORDS);
const LOG_KEY = "devbot_unknown_questions";

class DevBot {
  constructor(data = INTENTS, threshold = THRESHOLD) {
    this.intents = data.intents;
    this.fallback = data.fallback;
    this.threshold = threshold;
    this.patterns = [];
    this.tags = [];
    for (const intent of this.intents) {
      for (const pattern of intent.patterns) {
        this.patterns.push(pattern);
        this.tags.push(intent.tag);
      }
    }
    this.model = Tfidf.fit(this.patterns, STOPS);
  }

  // Returns the reply plus how it was chosen, so the page can explain it.
  match(message) {
    const vector = Tfidf.transform(this.model, message.toLowerCase());
    const scores = this.model.rows.map((row) => Tfidf.dot(vector, row));
    let best = 0;
    for (let i = 1; i < scores.length; i++) if (scores[i] > scores[best]) best = i;
    const score = scores[best];
    if (score < this.threshold) return { known: false, score, tag: null, pattern: null };
    return { known: true, score, tag: this.tags[best], pattern: this.patterns[best] };
  }

  reply(message, random = Math.random) {
    const m = this.match(message);
    if (!m.known) return { ...m, text: this.fallback };
    const intent = this.intents.find((i) => i.tag === m.tag);
    return { ...m, text: intent.responses[Math.floor(random() * intent.responses.length)] };
  }
}

// ---- Page wiring (browser only) ----
if (typeof document !== "undefined") {
  const $ = (id) => document.getElementById(id);
  const bot = new DevBot();
  const log = $("log");
  const form = $("form");
  const input = $("message");

  const readUnknown = () => {
    try { return JSON.parse(localStorage.getItem(LOG_KEY)) || []; } catch { return []; }
  };
  const writeUnknown = (list) => {
    try { localStorage.setItem(LOG_KEY, JSON.stringify(list.slice(-50))); } catch { /* private mode */ }
  };

  function renderUnknown() {
    const list = readUnknown();
    const ul = $("unknown");
    ul.innerHTML = "";
    if (!list.length) ul.innerHTML = '<li class="empty">Nothing yet — try asking DevBot something it was never taught.</li>';
    for (const q of list.slice().reverse()) {
      const li = document.createElement("li");
      li.textContent = q;
      ul.appendChild(li);
    }
  }

  function bubble(who, text, meta) {
    const row = document.createElement("div");
    row.className = "msg " + who;
    const b = document.createElement("div");
    b.className = "bubble";
    b.textContent = text;
    row.appendChild(b);
    if (meta) {
      const m = document.createElement("div");
      m.className = "meta";
      m.textContent = meta;
      row.appendChild(m);
    }
    log.appendChild(row);
    log.scrollTop = log.scrollHeight;
  }

  function send(text) {
    const message = text.trim();
    if (!message) return;
    bubble("you", message);
    const r = bot.reply(message);
    const meta = r.known
      ? `intent: ${r.tag} · closest pattern "${r.pattern}" · similarity ${r.score.toFixed(2)}`
      : `best similarity ${r.score.toFixed(2)} < ${bot.threshold} → admits it doesn't know · question logged`;
    setTimeout(() => bubble("bot" + (r.known ? "" : " unsure"), r.text, meta), 220);
    if (!r.known) {
      writeUnknown([...readUnknown(), message]);
      renderUnknown();
    }
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    send(input.value);
    input.value = "";
  });
  for (const chip of document.querySelectorAll("[data-ask]")) {
    chip.addEventListener("click", () => send(chip.dataset.ask));
  }
  $("clear-unknown").addEventListener("click", () => {
    writeUnknown([]);
    renderUnknown();
  });

  $("intent-count").textContent = bot.intents.length;
  $("pattern-count").textContent = bot.patterns.length;
  bubble("bot", bot.intents.find((i) => i.tag === "greeting").responses[0], "DevBot · TF-IDF intent matcher");
  renderUnknown();
}

if (typeof module !== "undefined") module.exports = { DevBot };
