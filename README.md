# 🚀 LangGraph Agent System

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![CI/CD](https://github.com/yourusername/LangGraph_Agent_System/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/yourusername/LangGraph_Agent_System/actions)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-orange)](https://python.langchain.com/docs/langgraph)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready, Dockerized monorepo showcasing advanced AI engineering, multi-agent orchestration, and end-to-end data science pipelines. Built with **LangGraph**, **Gemini**, **XGBoost**, and **Flask/Streamlit**.

---

## 🌟 Overview

**LangGraph Agent System** is a comprehensive showcase of modern AI applications. It unifies five distinct projects under a single orchestrated microservices architecture. 

The core of the system is a **4-Agent LangGraph Workflow** (Planner → Architect → Worker → Reviewer) designed for self-healing code generation and task execution.

### 📦 Key Sub-Projects

1. **📈 AI Trading Agent (3-Agent System)**: A crypto trading bot (BTC, ETH, SOL) using LangGraph. Features a Technical Agent, a Sentiment Agent (with real-time news scraping), and a Risk Manager that dynamically adjusts portfolio allocation based on Whale Alerts.
2. **🏠 Real Estate Price Prediction**: An end-to-end Data Science pipeline. Scrapes real estate data via Playwright (bypassing Cloudflare), cleans outliers using Local Z-Scores, engineers features using Regex, and predicts prices using a segmented XGBoost model via a Flask Web App.
3. **🦸‍♂️ Jarvis RPG Assistant**: A gamified personal assistant dashboard built with Streamlit.
4. **🃏 SillyTavern World Card Generator**: An AI-powered Streamlit app that generates JSON world cards for roleplaying platforms.
5. **🎁 Airdrop Guerrilla**: Automated crypto airdrop farming bots for Twitter, Discord, and Zealy using secure wallet management.

---

## 🏗️ Architecture

The project follows a Monorepo structure, containerized via Docker and orchestrated with `docker-compose`. For detailed architectural decisions, data flow diagrams, and LangGraph schematics, please read the [ARCHITECTURE.md](ARCHITECTURE.md).

---

## 🚀 Getting Started

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- (Optional) Python 3.10+ if running locally without Docker.

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/LangGraph_Agent_System.git
cd LangGraph_Agent_System
```

### 2. Configure Environment Variables
Copy the template and add your API keys:
```bash
cp .env.example .env
# Edit .env and insert your Gemini API Key, Binance Testnet keys, etc.
```

### 3. Run via Docker Compose (Production / Showcase Mode)
Build and spin up the entire system (Web Apps, Dashboards, and Background Daemons):
```bash
docker-compose up -d --build
```

**Access the Services:**
- 🏠 **Real Estate App:** [http://localhost:5000](http://localhost:5000)
- 🃏 **SillyTavern Generator:** [http://localhost:8501](http://localhost:8501)
- 🦸‍♂️ **Jarvis Dashboard:** [http://localhost:8502](http://localhost:8502)

### 4. Run via Local Dashboard (Developer Mode)
If you prefer running specific scripts interactively on your host machine:
```bash
pip install -r requirements.txt
python dashboard.py
```
This will open an interactive CLI dashboard to trigger backtests, live trading, or scrape data manually.

---

## 🛠️ CI/CD & Deployment

This project uses **GitHub Actions** for Continuous Integration. Every push to the `main` branch triggers:
- **Linting**: Python syntax checking via `flake8`.
- **Docker Build Test**: Ensures the multi-stage `Dockerfile` compiles successfully.

For deployment, an Nginx reverse proxy configuration is provided in `nginx/nginx.conf` for hosting on a VPS (AWS EC2, DigitalOcean) with SSL termination via Certbot.

---

## 💡 Tech Stack

- **AI & LLMs:** LangChain, LangGraph, Gemini 2.5 Flash / 3.1 Pro, OpenAI Proxy.
- **Data Science:** Pandas, NumPy, Scikit-learn, XGBoost, Folium.
- **Web Scraping:** Playwright, BeautifulSoup, CCXT, YFinance.
- **Backend & UI:** Flask, Streamlit.
- **DevOps:** Docker, Docker Compose, GitHub Actions, Nginx.

---

## 📝 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
