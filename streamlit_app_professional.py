import streamlit as st
import pandas as pd
import datetime
from chatbot import FinancialChatbot
from Savings_Analyser import SavingsAnalyzer  # uses Granite (silent fallback)

# ---------- INITIAL SETUP ----------
def init_chatbot():
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = FinancialChatbot()
    return st.session_state.chatbot

def init_analyzer():
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = SavingsAnalyzer()
    return st.session_state.analyzer

if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame(
        columns=["Date", "Type", "Category", "Description", "Amount"]
    )
if "budgets" not in st.session_state:
    st.session_state.budgets = {
        "Food": 5000,
        "Transport": 2000,
        "Rent": 10000,
        "Shopping": 3000,
        "Bills": 2500,
        "Other": 1500
    }

st.set_page_config(page_title="PocketSage | AI Finance Dashboard", page_icon="💎", layout="wide")

# ---------- GLOBAL STYLE ----------
st.markdown("""
<style>
body, .main {
    background: linear-gradient(180deg, #020617 0%, #0f172a 100%) !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif;
}
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 1200px !important;
    margin: auto;
}
.header {
    text-align: center;
    margin-bottom: 2rem;
}
.header h1 {
    font-size: 2.8rem;
    font-weight: 800;
    color: #f9fafb;
}
.header h1 span {
    color: #60a5fa;
}
.header p {
    color: #d1d5db;
    margin-top: -0.4rem;
}

/* ---------------- NAV BUTTONS ---------------- */
.nav-buttons {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 2.5rem;
}
.nav-buttons button {
    background: #1e293b;
    color: rgb(0,0,0) !important;
    border-radius: 10px;
    border: 1px solid #334155;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    transition: all 0.2s ease-in-out;
}
.nav-buttons button:hover {
    background: #2563eb;
    color: #000000 !important;
    transform: scale(1.05);
}
.nav-buttons button.active {
    background: #3b82f6 !important;
    color: #000000 !important;
    border: 1px solid #60a5fa;
}

/* ---------------- CARD DESIGN ---------------- */
.card {
    background: #0b1120;
    border-radius: 16px;
    padding: 2rem;
    color: #ffffff;
    box-shadow: 0 4px 25px rgba(0,0,0,0.8);
    margin-top: -0.5rem !important; /* move section a bit up */
}
.card h2 {
    color: #ffffff !important;
    font-weight: 700;
    margin-bottom: 1rem;
}

/* ---------------- METRIC STYLING ---------------- */
[data-testid="stMetricLabel"] {
    color: #ffffff !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    opacity: 1 !important;
    text-align: center !important;
}
[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
}

/* ---------------- FORM INPUTS ---------------- */
.stTextInput > div > div > input,
.stSelectbox > div > div > div,
.stNumberInput input,
.stDateInput input {
    background-color: #111827 !important;
    color: #ffffff !important;
    border-radius: 8px;
    border: 1px solid #334155;
}
.stTextInput label, .stSelectbox label, .stNumberInput label, .stDateInput label {
    color: #e2e8f0 !important;
}
.dataframe {
    background: #111827 !important;
    color: #ffffff !important;
}
.progress-label {
    margin-top: 0.8rem;
    color: #ffffff;
    font-weight: 500;
}

/* ---------------- FOOTER ---------------- */
.footer {
    position: fixed;
    right: 20px;
    bottom: 10px;
    background: #1e293b;
    padding: 6px 12px;
    border-radius: 8px;
    font-size: 0.8rem;
    color: #a5b4fc;
    box-shadow: 0 2px 5px rgba(0,0,0,0.4);
}
</style>
""", unsafe_allow_html=True)


# ---------- HEADER ----------
st.markdown("""
<div class="header">
    <h1>💎 <span>PocketSage</span></h1>
    <p>Your AI-Powered Finance Assistant</p>
</div>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.markdown("### 💎 Powered by IBM Granite")
st.sidebar.caption("AI engine running locally via IBM Granite 3.1 1B Instruct")

# ---------- NAVIGATION ----------
menu_items = ["🏠 Home", "💳 Transactions", "🎯 Budgets", "💡 Smart Savings", "🤖 Chat"]

if "active_page" not in st.session_state:
    st.session_state.active_page = "🏠 Home"

# Wrap nav buttons in a styled container
st.markdown("<div style='margin-bottom: 25px;'>", unsafe_allow_html=True)

cols = st.columns(len(menu_items))
for i, item in enumerate(menu_items):
    button_style = """
        <style>
        div[data-testid="stButton"] button {
            background-color: black !important;
            color: white !important;
            border-radius: 8px !important;
            border: 1px solid #1f2937 !important;
            font-weight: 600 !important;
            transition: all 0.2s ease-in-out;
        }
        div[data-testid="stButton"] button:hover {
            background-color: #111827 !important;
            color: #60a5fa !important;
            transform: scale(1.05);
        }
        </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)
    if cols[i].button(item, use_container_width=True):
        st.session_state.active_page = item

st.markdown("</div>", unsafe_allow_html=True)

chatbot = init_chatbot()
analyzer = init_analyzer()
page = st.session_state.active_page


# ---------- HOME ----------
if page == "🏠 Home":
    st.markdown('<div class="card"><h2>📊 Financial Overview</h2>', unsafe_allow_html=True)
    df = st.session_state.transactions
    total_income = df[df["Type"] == "Income"]["Amount"].sum()
    total_expense = df[df["Type"] == "Expense"]["Amount"].sum()
    balance = total_income - total_expense
    savings_rate = (balance / total_income * 100) if total_income > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("💰 Income", f"₹{total_income:,.2f}")
    with c2: st.metric("💸 Expense", f"₹{total_expense:,.2f}")
    with c3: st.metric("🏦 Balance", f"₹{balance:,.2f}")
    with c4: st.metric("📈 Savings Rate", f"{savings_rate:.1f}%")

    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- TRANSACTIONS ----------
elif page == "💳 Transactions":
    st.markdown('<div class="card"><h2>💳 Manage Transactions</h2>', unsafe_allow_html=True)
    with st.form("add_txn", clear_on_submit=True):
        date = st.date_input("Date", datetime.date.today())
        t_type = st.selectbox("Type", ["Income", "Expense"])
        category = st.selectbox("Category", list(st.session_state.budgets.keys()))
        desc = st.text_input("Description")
        amt = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")
        submitted = st.form_submit_button("➕ Add Transaction")
        if submitted:
            new_txn = pd.DataFrame([{
                "Date": date, "Type": t_type, "Category": category, "Description": desc, "Amount": amt
            }])
            st.session_state.transactions = pd.concat(
                [st.session_state.transactions, new_txn], ignore_index=True
            )
            st.session_state.updated_at = datetime.datetime.now().strftime("%H:%M:%S")
            st.success(f"Transaction added ✅ (Updated {st.session_state.updated_at})")
            st.rerun()

    if not st.session_state.transactions.empty:
        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(st.session_state.transactions, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ---------- BUDGETS ----------
elif page == "🎯 Budgets":
    st.markdown('<div class="card"><h2>🎯 Budgets Overview</h2>', unsafe_allow_html=True)

    df = st.session_state.transactions
    edit_mode = st.checkbox("🛠 Edit Budget Limits")

    # ----- Editable Budgets -----
    if edit_mode:
        st.write("Adjust your category budgets below:")
        new_budgets = {}
        for cat, limit in st.session_state.budgets.items():
            new_limit = st.number_input(f"{cat} Budget (₹)", min_value=0.0, value=float(limit), step=500.0)
            new_budgets[cat] = new_limit

        if st.button("💾 Save Changes", use_container_width=True):
            st.session_state.budgets = new_budgets
            st.success("✅ Budgets updated successfully!")
            st.session_state.updated_at = datetime.datetime.now().strftime("%H:%M:%S")
            st.rerun()

        st.markdown("---")

    # ----- Budget Visualization -----
    for cat, limit in st.session_state.budgets.items():
        spent = df[(df["Type"] == "Expense") & (df["Category"] == cat)]["Amount"].sum()
        percent = min(spent / limit if limit > 0 else 0, 1.0)
        remaining = limit - spent
        color = "🟢" if remaining > (0.3 * limit) else ("🟠" if remaining > 0 else "🔴")

        st.markdown(
            f'<div class="progress-label">{color} {cat}: ₹{spent:,.2f} / ₹{limit:,.2f} '
            f'(<b>{100 * percent:.1f}%</b> used)</div>', unsafe_allow_html=True)
        st.progress(percent)

    if "updated_at" in st.session_state:
        st.caption(f"🕒 Last updated: {st.session_state.updated_at}")

    st.markdown('</div>', unsafe_allow_html=True)


# ---------- SMART SAVINGS ----------
elif page == "💡 Smart Savings":
    st.markdown('<div class="card"><h2>💡 Smart Savings Analyzer</h2>', unsafe_allow_html=True)
    salary = st.number_input("Monthly Salary (₹)", min_value=0.0, step=1000.0)
    monthly_expense = st.number_input("Average Monthly Expenses (₹)", min_value=0.0, step=500.0)
    goal_duration = st.slider("Savings Duration (months)", 1, 60, 12)
    debt = st.number_input("Monthly Loan/Debt Payments (₹)", min_value=0.0, step=500.0)
    st.markdown("---")

    if salary > 0:
        insight = analyzer.analyze_savings(salary, monthly_expense, goal_duration, debt)
        st.markdown(f"**🧠 AI Insight:** {insight}")
    else:
        st.info("Enter your salary to calculate savings potential.")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- CHAT ----------
elif page == "🤖 Chat":
    st.markdown("""
        <div style="background-color:#0f172a;padding:25px;border-radius:15px;margin-bottom:20px;">
            <h2 style="color:white;text-align:center;">💬 Chat with <span style="color:#60a5fa;">PocketSage</span></h2>
            <p style="color:#93c5fd;text-align:center;">Your emotionally intelligent finance companion 💸</p>
        </div>
    """, unsafe_allow_html=True)

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hey there! I’m your AI finance buddy 💸", "emotion": "Calm"}
        ]

    # Emotion color map
    emotion_colors = {
        "Happy": "🟢",
        "Calm": "🩵",
        "Motivated": "💪",
        "Frustrated": "🟠",
        "Stressed": "🔴",
        "Sad": "🔵",
        "Confused": "🟣",
        "Neutral": "⚪",
        "Error": "⚠️"
    }

    # Chat display
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(
                f"""
                <div style="
                    background-color:white;
                    color:#1e3a8a;
                    padding:12px 18px;
                    border-radius:15px 15px 0 15px;
                    margin:10px 20px 10px auto;
                    width:fit-content;
                    max-width:80%;
                    box-shadow:0 2px 8px rgba(0,0,0,0.1);
                    ">
                    <b>You:</b> {msg['content']}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            icon = emotion_colors.get(msg.get("emotion", "Neutral"), "⚪")
            st.markdown(
                f"""
                <div style="
                    background:linear-gradient(135deg,#1e3a8a,#1e40af);
                    color:white;
                    padding:14px 18px;
                    border-radius:15px 15px 15px 0;
                    margin:10px auto 10px 20px;
                    width:fit-content;
                    max-width:80%;
                    box-shadow:0 2px 8px rgba(0,0,0,0.2);
                    ">
                    <div style="font-size:13px;opacity:0.85;margin-bottom:4px;">
                        {icon} <b>User Emotion:</b> {msg.get('emotion','Neutral')}
                    </div>
                    <div style="font-size:15px;">{msg['content']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # User input
    if user := st.chat_input("Ask me anything about your finances..."):
        st.session_state.chat_history.append({"role": "user", "content": user})

        with st.spinner("PocketSage is thinking 💭..."):
            reply = chatbot.ask(user)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": reply["response"],
            "emotion": reply["emotion"]
        })

        st.rerun()


# ---------- FOOTER ----------
st.markdown('<div class="footer">💎 Powered by IBM Granite | PocketSage AI</div>', unsafe_allow_html=True)
