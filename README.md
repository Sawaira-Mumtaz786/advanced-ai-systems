# 🧪 Advanced AI Systems: Evaluation & Multi-Agent Orchestration
Click to see Live Demo   https://advanced-ai-systems-fsz7jtqn7o8shhntitckpp.streamlit.app/
A portfolio project showcasing advanced AI engineering skills, including LLM-as-judge evaluation and multi-agent state machines with human-in-the-loop routing.

## 🚀 Features

### 1. LLM Evaluation Dashboard
- Automated evaluation of LLM outputs using the **LLM-as-judge** methodology.
- Scores outputs on **Faithfulness** (is it hallucinating?) and **Answer Relevance**.
- Interactive Streamlit UI with Plotly charts.
- Powered by Groq (`openai/gpt-oss-20b`).

### 2. LangGraph Multi-Agent State Machine
- **Agent A (Structurer):** Converts messy text into clean JSON.
- **Agent B (Validator):** Applies business rules (e.g., flagging amounts > 1000).
- **Human-in-the-Loop:** Automatically pauses execution at a checkpoint for manual approval when anomalies are detected.

## 🛠️ Tech Stack
- **Language:** Python 3.11
- **LLM Provider:** Groq (Free Tier)
- **Agent Framework:** LangGraph
- **UI/Visualization:** Streamlit, Plotly, Pandas
- **Environment Management:** `uv` + `venv`

## 📦 Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Sawaira-Mumtaz786/advanced-ai-systems.git
   cd advanced-ai-systems

   Create and activate a virtual environment:

bash
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
Install dependencies:

bash
pip install -r requirements.txt
Set up environment variables:
Create a .env file in the root and add your Groq API key:

env
GROQ_API_KEY=your_groq_api_key_here
Run the Streamlit Dashboard:

bash
cd evaluations
streamlit run app_dash.py
Run the Multi-Agent System:

bash
cd agents
python multi_agent.py

👩‍💻 Author

Sawaira Mumtaz - AI Software Engineer
