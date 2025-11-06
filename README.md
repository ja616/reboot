# 💎 PocketSage — AI-Powered Personal Finance Assistant

**PocketSage (Reboot)** is an AI-powered personal finance dashboard built with **Streamlit**, designed to help users manage their budgets, track transactions, and receive smart AI insights.  
It integrates **IBM Granite (local)** and **Hugging Face models (API)** for financial analysis and natural language understanding — delivering intelligent, private, and interactive finance management.

---

## 🚀 Features

### 🏠 **Home Dashboard**
- Shows **Income, Expense, Balance, and Savings Rate**.
- Clean financial summary cards.
- Auto-updates when transactions are added.
- Interactive expense visualizations.

### 💳 **Transactions**
- Add, view, and manage income/expense entries easily.
- Real-time transaction updates.
- Clean tabular view powered by Streamlit DataFrames.

### 🎯 **Budgets**
- Create and adjust **custom budget limits** per category.
- Visualize your spending progress.
- Color-coded progress bars:
  - 🟢 Within budget  
  - 🟠 Nearing limit  
  - 🔴 Exceeded

### 💡 **Smart Savings Analyzer**
- Enter salary, expenses, and debt — get **AI-generated savings advice**.
- Powered by **SavingsAnalyzer** (uses IBM Granite fallback logic).
- Predicts your long-term savings potential.

### 🤖 **PocketSage Chat**
- Talk to your AI finance assistant in natural language.
- Emotion-aware responses (e.g., Calm, Motivated, Stressed).
- Uses **IBM Granite locally** and **Hugging Face API** as fallback.
- Example queries:
  - “How much did I spend on food?”
  - “Summarize my monthly expenses.”
  - “Give me a 3-month savings plan.”

---

## 🧠 Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend/UI** | [Streamlit](https://streamlit.io/) |
| **AI/LLM Models** | IBM Granite (Local) + Hugging Face API |
| **Data Handling** | Pandas, ChromaDB |
| **Visualization** | Streamlit Charts |
| **Environment Config** | `.env` file for keys and model setup |
| **Version Control** | Git + GitHub |

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/ja616/reboot.git
cd reboot
