import streamlit as st
import chromadb
from groq import Groq
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Configuration
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    st.error(" GROQ_API_KEY not found in .env file. Please add your API key.")
    st.stop()

# Initialize ChromaDB client
@st.cache_resource
def get_chroma_client():
    return chromadb.Client()

client = get_chroma_client()

# CSV file configuration
CSV_FILE_NAME = "products.csv"
COLLECTION_NAME = "ecommerce_products"

# Load and process data
@st.cache_data
def load_data():
    """Load data from CSV file"""
    try:
        df = pd.read_csv(CSV_FILE_NAME)
        return df
    except FileNotFoundError:
        st.error(f" {CSV_FILE_NAME} file not found. Please ensure the file exists in the project directory.")
        st.stop()

def add_data_to_chromadb(df):
    """Add product data to ChromaDB collection"""
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "E-commerce product catalog with specifications and pricing"}
    )
    
    # Check if collection already has data
    if collection.count() > 0:
        return collection
    
    # Prepare documents for ChromaDB
    documents = []
    metadatas = []
    ids = []
    
    for idx, row in df.iterrows():
        # Create detailed product document
        doc_text = f"""
        Product: {row['name']}
        Brand: {row['brand']}
        Category: {row['category']}
        Price: {row['price_lkr']} LKR
        Stock Available: {row['stock']} units
        Rating: {row['rating']}/5.0
        Features: {row['features']}
        Description: {row['description']}
        Colors: {row['color_options']}
        Warranty: {row['warranty']}
        """
        
        documents.append(doc_text.strip())
        
        # Store metadata
        metadatas.append({
            "product_id": row['product_id'],
            "name": row['name'],
            "category": row['category'],
            "brand": row['brand'],
            "price_lkr": str(row['price_lkr']),
            "stock": str(row['stock']),
            "rating": str(row['rating'])
        })
        
        ids.append(row['product_id'])
    
    # Add to collection
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    return collection

def search_products(query, n_results=5):
    """Search products based on query"""
    collection = client.get_collection(COLLECTION_NAME)
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results

def get_conversation_context(messages, max_history=5):
    """Build conversation context from chat history for memory"""
    recent_messages = messages[-max_history:] if len(messages) > max_history else messages
    context = ""
    for msg in recent_messages:
        role = "Customer" if msg["role"] == "user" else "Assistant"
        context += f"{role}: {msg['content']}\n"
    return context

def generate_response_with_memory(query, product_context, conversation_history):
    """Generate response using Groq LLM with conversation memory"""
    groq_client = Groq(api_key=API_KEY)
    
    # Build conversation context for memory
    memory_context = get_conversation_context(conversation_history)
    
    system_message = f"""You are ShopBot, a friendly and knowledgeable e-commerce shopping assistant. Your goal is to help customers find the perfect products and answer their questions.

CONVERSATION HISTORY (for context and memory):
{memory_context}

RELEVANT PRODUCT INFORMATION:
{product_context}

YOUR CAPABILITIES:
1. Product Recommendations - Suggest products based on needs, budget, and preferences
2. Price Comparisons - Compare products and help find the best value
3. Detailed Information - Provide specs, features, availability, and warranty details
4. Stock Availability - Check if items are in stock
5. Memory - Remember the conversation context and previous questions

GUIDELINES:
- Be conversational, friendly, and enthusiastic about helping
- Provide specific product names, prices in LKR, and key features
- When comparing products, highlight pros and cons
- If asked about previous messages, use the conversation history
- Suggest alternatives if a product is out of stock or over budget
- Ask clarifying questions if the request is ambiguous
- Format responses clearly with bullet points when listing multiple items
- Always mention stock availability for products
- Include color options when relevant
- Mention warranty information when discussing electronics

SPECIAL INSTRUCTIONS:
- If customer mentions budget constraints, respect their budget
- If they ask "what did I ask before" or similar, refer to conversation history
- Build on previous interactions naturally
- Be honest if a product isn't available or suitable

Remember: You're here to create a great shopping experience!"""

    completion = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": query}
        ],
        temperature=0.7,
        max_tokens=1024,
        top_p=0.9,
        stream=False,
    )
    
    return completion.choices[0].message.content

# Streamlit UI
def main():
    st.set_page_config(
        page_title="ShopBot - Your Shopping Assistant",
        page_icon="🛒",
        layout="wide"
    )
    
    # Custom CSS for better UI
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        .sub-header {
            text-align: center;
            color: #666;
            margin-bottom: 2rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="main-header">🛒 ShopBot - Your AI Shopping Assistant</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Find the perfect products with intelligent recommendations and instant answers!</p>', unsafe_allow_html=True)
    
    # Load data
    data_df = load_data()
    
    # Initialize ChromaDB with data
    with st.spinner("🔄 Loading product catalog..."):
        collection = add_data_to_chromadb(data_df)
    
    # Sidebar with product catalog overview
    with st.sidebar:
        st.header("📊 Product Catalog Overview")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Products", len(data_df))
        with col2:
            in_stock = len(data_df[data_df['stock'] > 0])
            st.metric("In Stock", in_stock)
        
        # Categories breakdown
        st.subheader("📦 Categories")
        category_counts = data_df['category'].value_counts()
        for category, count in category_counts.items():
            st.write(f"🔹 **{category}**: {count} items")
        
        # Price range
        st.subheader("💰 Price Range")
        min_price = data_df['price_lkr'].min()
        max_price = data_df['price_lkr'].max()
        avg_price = data_df['price_lkr'].mean()
        st.write(f"**Lowest**: LKR {min_price:,.0f}")
        st.write(f"**Highest**: LKR {max_price:,.0f}")
        st.write(f"**Average**: LKR {avg_price:,.0f}")
        
        # Top brands
        st.subheader("🏷️ Top Brands")
        brand_counts = data_df['brand'].value_counts().head(5)
        for brand, count in brand_counts.items():
            st.write(f"• {brand}: {count} products")
        
        st.divider()
        
        # Example queries
        st.subheader("💡 Try Asking:")
        example_queries = [
            "Show me laptops under 500,000 LKR",
            "What's the best smartphone for photography?",
            "Compare iPhone 15 Pro Max vs Samsung S23 Ultra",
            "Do you have wireless headphones in stock?",
            "What gaming products do you have?",
            "Recommend a tablet for students",
            "What are the top-rated products?",
            "Show me Apple products",
            "Which TV has the best value for money?",
            "I need a portable speaker for outdoor use"
        ]
        
        for query in example_queries:
            if st.button(query, key=query, use_container_width=True):
                # Set the query in session state to trigger it
                st.session_state.suggested_query = query
                st.rerun()
        
        st.divider()
        
        # Memory indicator
        st.subheader("🧠 Conversation Memory")
        if "messages" in st.session_state:
            msg_count = len([m for m in st.session_state.messages if m["role"] == "user"])
            st.write(f"💬 Messages exchanged: **{msg_count}**")
            st.caption("ShopBot remembers your conversation!")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.session_state.suggested_query = None
            st.rerun()
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        welcome_msg = """👋 **Welcome to ShopBot!** 

I'm your personal shopping assistant, here to help you find the perfect products from our catalog of electronics, gadgets, and accessories.

**I can help you with:**
- 🔍 Finding products that match your needs and budget
- 📊 Comparing different products
- 💡 Getting detailed specifications and features
- ✅ Checking stock availability
- 🎯 Personalized recommendations
- 💬 Remembering our conversation to provide better assistance

**What would you like to shop for today?**"""
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Handle suggested query from sidebar
    suggested_query = st.session_state.get("suggested_query")
    if suggested_query:
        user_query = suggested_query
        st.session_state.suggested_query = None  # Clear after using
    else:
        user_query = st.chat_input("Ask about products, prices, features, or get recommendations...")
    
    if user_query:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Searching products and preparing response..."):
                # Search relevant products
                search_results = search_products(user_query, n_results=6)
                
                # Prepare context from search results
                product_context = "\n\n".join(search_results["documents"][0])
                
                # Generate response with conversation memory
                response = generate_response_with_memory(
                    user_query, 
                    product_context,
                    st.session_state.messages
                )
                
                st.markdown(response)
                
                # Show relevant products as expandable cards
                if search_results["metadatas"][0]:
                    st.divider()
                    st.caption("📦 Related Products:")
                    
                    cols = st.columns(3)
                    for idx, metadata in enumerate(search_results["metadatas"][0][:6]):
                        with cols[idx % 3]:
                            with st.expander(f"🛍️ {metadata['name']}", expanded=False):
                                st.write(f"**Brand**: {metadata['brand']}")
                                st.write(f"**Category**: {metadata['category']}")
                                st.write(f"**Price**: LKR {metadata['price_lkr']}")
                                st.write(f"**Stock**: {metadata['stock']} units")
                                st.write(f"**Rating**: ⭐ {metadata['rating']}/5.0")
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()