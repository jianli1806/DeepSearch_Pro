# 🕵️ DeepSearch Pro: Autonomous AI Research Agent

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-Stateful_Agent-orange)
![Llama 3](https://img.shields.io/badge/Model-Llama_3-purple)
![License](https://img.shields.io/badge/License-MIT-green)

**DeepSearch Pro** is an autonomous agentic system designed to perform in-depth topic research. Unlike traditional RAG (Retrieval-Augmented Generation) systems that rely on static databases, DeepSearch Pro dynamically plans search strategies, browses the live web, and synthesizes information into comprehensive reports with citations.

## 🧠 Key Features

* **Agentic Workflow:** Utilizes **LangGraph** to orchestrate a cyclic "Plan → Execute → Reflect" workflow.
* **Real-time Web Retrieval:** Integrated with **Tavily API** to bypass legacy knowledge cutoffs and access real-time data.
* **Cost-Efficient Architecture:** Powered by **Meta Llama 3** (via Groq LPU), achieving 10x lower inference latency compared to GPT-4.
* **State Management:** Maintains context across multi-step reasoning processes to ensure coherence.
* **Professional UI:** Built with **Streamlit** for a seamless, interactive user experience.

## 🏗️ Architecture

The system follows a multi-agent architecture:


graph LR
    User[User Input] --> Planner
    Planner[🧠 Planner Node] -->|Generate Queries| Search[🕵️ Research Node]
    Search -->|Fetch & Summarize| Context[Context Window]
    Context --> Writer[✍️ Writer Node]
    Writer -->|Final Report| Output[Markdown Report]

🚀 Quick Start
Prerequisites
Python 3.9+

API Keys for Groq & Tavily

Installation
Clone the repository

Bash

git clone https://github.com/jayleecoder1809/DeepSearch_Pro.git
cd DeepSearch_Pro
Install dependencies

Bash

pip install -r requirements.txt
Configure Environment Create a .env file in the root directory:

Code snippet

GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
Run the Application

Bash

streamlit run main.py
🛠️ Tech Stack
Orchestration: LangGraph, LangChain

LLM: Meta Llama 3.3 (via Groq Cloud)

Search Engine: Tavily AI Search

Frontend: Streamlit

Environment: Python-dotenv

📄 License
Distributed under the MIT License.
