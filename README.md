# 🛒 E-commerce Chatbot with Memory

An intelligent shopping assistant powered by **Streamlit**, **ChromaDB**, and **Groq LLM** (llama-3.1-8b-instant).

## ✨ Features

- 🔍 Smart product search with RAG (Retrieval Augmented Generation)
- 🧠 Conversation memory for context-aware responses
- 💡 AI-powered product recommendations
- 📊 Product comparison and detailed information
- ✅ Real-time stock availability checking
- 🎨 Beautiful, interactive UI

---

## 📦 Dependencies

```txt
streamlit>=1.31.0
chromadb>=0.4.22
groq>=0.4.2
python-dotenv>=1.0.0
pandas>=2.1.4
```

---

## 🚀 Setup Instructions

### 1️⃣ Install Dependencies

**Option A: Using uv (Recommended)**
```bash
uv add streamlit chromadb groq python-dotenv pandas
```

**Option B: Using pip**
```bash
pip install -r requirements.txt
```

### 2️⃣ Configure API Key

1. Get your free Groq API key from [https://console.groq.com](https://console.groq.com)
2. Create a `.env` file in the project root:

```env
GROQ_API_KEY=your-groq-api-key-here
```

### 3️⃣ Run the Application

**Using uv:**
```bash
uv run streamlit run app.py
```

**Using Python:**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📁 Project Structure

```
Q3_Chatbot/
├── app.py              # Main application
├── products.csv        # Product dataset (25 items)
├── .env               # API key (DO NOT COMMIT)
├── .env.example       # Environment template
├── requirements.txt   # Dependencies
├── .gitignore        # Git ignore rules
└── README.md         # This file
```

---

## 💬 Usage Examples

Try asking:
- "Show me laptops under 500,000 LKR"
- "Compare iPhone 15 Pro Max vs Samsung S23 Ultra"
- "What's the best smartphone for photography?"
- "Do you have wireless headphones in stock?"
- "Recommend a tablet for students"


## 🛠️ Troubleshooting

**Error: "GROQ_API_KEY not found"**
- Ensure `.env` file exists
- Check API key format (no quotes)
- Verify key at https://console.groq.com

**Error: "products.csv not found"**
- Ensure CSV is in same directory as app.py
- Check filename is exactly `products.csv`

**Port already in use:**
```bash
streamlit run app.py --server.port 8502
```

---

## 👨‍💻 Tech Stack

- **Frontend:** Streamlit
- **LLM:** Groq (llama-3.1-8b-instant)
- **Vector DB:** ChromaDB
- **Language:** Python 3.10+

---

## 📊 Dataset

Contains 25 products across categories:
- Smartphones, Laptops, Headphones, TVs
- Cameras, Gaming, Wearables, Accessories
- Price range: LKR 12,990 - 749,990

