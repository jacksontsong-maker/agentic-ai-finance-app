import streamlit as st
import sqlite3
import pandas as pd
from openai import OpenAI
import os

# Initialize OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Connect to DB
conn = sqlite3.connect("expenses.db", check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists (important for cloud)
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    category TEXT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

st.title("💰 Personal Finance Dashboard")

# ➕ Add Expense Section
st.subheader("➕ Add Expense")

amount = st.number_input("Amount", min_value=0.0)
category = st.selectbox("Category", ["food", "transport", "shopping", "bills", "other"])

if st.button("Add Expense"):
    cursor.execute(
        "INSERT INTO expenses (amount, category) VALUES (?, ?)",
        (amount, category)
    )
    conn.commit()
    st.success("Expense added!")
    st.rerun()

# Load data
df = pd.read_sql_query("SELECT * FROM expenses", conn)

if df.empty:
    st.warning("No expenses recorded yet.")
else:
    # Total spending
    total = df["amount"].sum()
    st.metric("Total Spending", f"${total:.2f}")

    # Category breakdown
    st.subheader("📊 Spending by Category")
    category_df = df.groupby("category")["amount"].sum()
    st.bar_chart(category_df)

    st.subheader("📊 Category Percentage")

    percent_df = (category_df / total * 100).round(1)
    st.write(percent_df)

    # Daily trend
    st.subheader("📈 Daily Spending Trend")
    df["date"] = pd.to_datetime(df["date"])
    daily = df.groupby(df["date"].dt.date)["amount"].sum()
    st.line_chart(daily)

    st.subheader("📊 Smart Insights")

    # Highest spending category
    top_category = category_df.idxmax()
    top_value = category_df.max()

    st.write(f"💸 Highest spending: {top_category} (${top_value:.2f})")

    # Simple risk flag
    if top_value / total > 0.5:
        st.warning(f"⚠️ Over 50% of spending is on {top_category}")

    # AI Insights
    st.subheader("🧠 AI Insights")

    data_summary = df.groupby("category")["amount"].sum().to_dict()

    prompt = f"""
    You are an AI CFO helping a user manage personal finances.

    Here is the user's spending data:
    Total spending: ${total}
    Category breakdown: {data_summary}

    Analyze and provide:

    1. Key insight (what stands out?)
    2. Risk detection (any unhealthy spending patterns?)
    3. Specific actionable advice (what should they do next?)
    4. One cost-saving opportunity
    5. Predict next month's spending trend (increase/decrease + reason)

    Be concise, practical, and slightly critical like a real CFO.
    """

    if not df.empty:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        st.write(response.choices[0].message.content)

    # Raw data
    st.subheader("📄 Expense Data")
    st.dataframe(df)

   # 🤖 AI CFO Chat (clean version)
    st.subheader("🤖 Ask Your AI CFO")

    # Initialize memory
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show chat history FIRST
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input (at bottom)
    user_input = st.chat_input("Ask your AI CFO...")

    if user_input:
        # Show user message immediately
        with st.chat_message("user"):
            st.markdown(user_input)

        # Save user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Prepare financial context
        data_summary = df.groupby("category")["amount"].sum().to_dict()
        total_spending = df["amount"].sum()

        system_prompt = f"""
    You are a personal AI CFO.

    User financial data:
    Total spending: ${total_spending}
    Category breakdown: {data_summary}

    Answer clearly, concisely, and practically.
    """

        messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages

        # Get AI response
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages
        )

        reply = response.choices[0].message.content

        # Show AI message immediately
        with st.chat_message("assistant"):
            st.markdown(reply)

        # Save AI message
        st.session_state.messages.append({"role": "assistant", "content": reply})