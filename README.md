# 🛒 NexaShop AI — Intelligent E-Commerce Shopping Assistant

> **NexaShop AI** is a conversational shopping assistant powered by RAG (Retrieval Augmented Generation), ChromaDB, and Groq LLM — built to help customers discover, compare, and choose the perfect product from a Sri Lankan electronics catalogue.

---

## ✨ Features

- 🔍 **Semantic Product Search** — ChromaDB vector search finds relevant products even with vague queries
- 🧠 **Conversational Memory** — retains context across turns for natural follow-up questions
- 💡 **AI Recommendations** — Groq LLM (llama-3.1-8b-instant) generates personalised suggestions
- 📊 **Product Comparison** — side-by-side feature and price breakdowns
- ✅ **Live Stock Check** — real-time availability from the product dataset
- 🎨 **Interactive Streamlit UI** — sidebar catalogue overview, clickable example queries, expandable product cards

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend / UI | Streamlit ≥ 1.52 |
| LLM Provider | Groq — `llama-3.1-8b-instant` |
| Vector Store | ChromaDB ≥ 1.4 |
| Data | Pandas + `products.csv` |
| Environment | python-dotenv |
| Package Manager | uv *(recommended)* or pip |
| Runtime | Python 3.13+ |

---

## 📁 Project Structure

```
NexaShop-AI/
├── app.py              # Main Streamlit application
├── products.csv        # Product catalogue (25 items, LKR pricing)
├── .env                # API key — ⚠️ DO NOT COMMIT
├── .env.example        # Environment variable template
├── pyproject.toml      # Project metadata & dependencies
├── uv.lock             # Locked dependency tree
├── .gitignore
└── README.md
```

---

## 📦 Dataset — `products.csv`

25 products across **9 categories**, priced in Sri Lankan Rupees (LKR):

| Category | Items |
|---|---|
| Smartphones | Samsung Galaxy S23 Ultra, iPhone 15 Pro Max |
| Laptops | Dell XPS 15, MacBook Pro 14 |
| Headphones | Sony WH-1000XM5, AirPods Pro 2nd Gen |
| TVs | Samsung 55" QLED, LG 65" OLED |
| Cameras | Canon EOS R6 Mark II, GoPro Hero 12 |
| Gaming | PlayStation 5, Xbox Series X, Razer BlackWidow V4 |
| Wearables | Apple Watch Series 9, Fitbit Charge 6 |
| Speakers | Bose SoundLink Revolve+, JBL Flip 6 |
| Accessories / Storage / Networking | Anker, Logitech, TP-Link, WD, Samsung SSD… |

**Price range:** LKR 12,990 — LKR 749,990

Each row includes: `product_id`, `name`, `brand`, `category`, `price_lkr`, `stock`, `rating`, `features`, `description`, `color_options`, `warranty`

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/NexaShop-AI.git
cd NexaShop-AI
```

### 2. Install dependencies

**Option A — uv (recommended)**
```bash
uv add streamlit chromadb groq python-dotenv pandas
```

**Option B — pip**
```bash
pip install streamlit chromadb groq python-dotenv pandas
```

### 3. Set up your API key

Get a free Groq API key from [console.groq.com](https://console.groq.com), then create `.env`:

```env
GROQ_API_KEY=your-groq-api-key-here
```

### 4. Run

```bash
# with uv
uv run streamlit run app.py

# with python
streamlit run app.py
```

App opens at **http://localhost:8501**

---

## 💬 Example Queries

```
"Show me laptops under 500,000 LKR"
"Compare iPhone 15 Pro Max vs Samsung S23 Ultra"
"What's the best smartphone for photography?"
"Do you have wireless headphones in stock?"
"Recommend a tablet for students"
"Which TV has the best value for money?"
"Show me all Apple products"
```

---

## 🛠️ Troubleshooting

| Error | Fix |
|---|---|
| `GROQ_API_KEY not found` | Create `.env` with your key (no quotes around value) |
| `products.csv not found` | Ensure CSV is in the same directory as `app.py` |
| Port already in use | `streamlit run app.py --server.port 8502` |

---

## 👩‍💻 Author

**Ayeshi Jayarathna**
