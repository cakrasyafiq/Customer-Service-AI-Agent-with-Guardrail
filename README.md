# AI Customer Service Agent with PII Guardrail

An **AI Customer Service Agent** powered by **Google Gemini** (via Google ADK) and protected by a **multi-layer PII guardrail** system.  
This project ensures user privacy by detecting and redacting sensitive information using **regex-based rules** and an **external NER service API** before sending input to the LLM.

---

## ✨ Key Features

- 🤖 AI Customer Service Agent using **Google Gemini**
- 🛡️ Multi-layer **PII Guardrail**
  - Regex-based entity detection (EMAIL, PHONE, ID, etc.)
  - NER-based detection via external **NER API**
- ✂️ Automatic redaction with entity-aware masking  
  (`[REDACTED_PERSON]`, `[REDACTED_EMAIL]`, etc.)
- 🔌 Modular design (Agent, Guardrail, Metrics)
- 🧠 Privacy-first architecture for LLM-based systems

---

## 🏗️ Architecture Overview

```
AI Agent Start (Google ADK sessions)

   ↓

User Input

   ↓ -> Str

Guardrail Layer (via before_model_callback)
 ├── Regex Detection
 ├── NER API Call
 └── Entity-based Masking

   ↓ -> Str (Safe user input)

LLM Model (Gemini 2.5 flash)

   ↓

Safe AI Response
```

---

## 🗂️ Project Structure

```
ai_agent/
├── customer_service_agent/
│   ├── agent.py 
│   ├── guardrail/
│   │   ├── guardrail.py         # PII detection & masking logic
│   │   └── test_guardrail.py    # Guardrail testing script
│   ├── metrics/
│   │   └── metrics.py           # CPU, memory, latency tracking
│   └── __init__.py                  # Entry point
│   └──.env.example
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Tech Stack

- **Python** 3.10+
- **Google ADK**
- **Google Gemini**
- **FastAPI** (NER API integration)
- **spaCy** (via external NER service)
- **psutil** (resource monitoring)
- **python-dotenv**

---

## 📦 Installation

### 1. Clone Repository
```bash
git clone https://github.com/USERNAME/ai-agent-with-pii-guardrail.git
cd ai-agent-with-pii-guardrail
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

Activate:

**Windows**
```bash
venv\Scripts\activate
```

**Linux / macOS**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Copy the `.env.example` and change it to `.env` file. Or create a `.env` file like:

```env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=YOUR_API_KEY_HERE
NER_SERVICE_URL=http://127.0.0.1:8001/ner
```
fill in with your Gemini API key

📌 `.env` is ignored by Git for security reasons.

---

## ▶️ Running the AI Agent

Make sure the **NER API service is running first**. 
Access the API repo here: https://github.com/cakrasyafiq/API-NER-for-People-s-Names-Address

Then run:

```bash
adk web
```

---

## 🛡️ Guardrail Behavior Example

### User Input
```
Halo, saya Putra Syafiq dengan nomor 082112239199 dan email user@gmail.com
```

### Guardrail Output
```
Allowed : False
Reason  : PII detected: PERSON, PHONE, EMAIL
Safe    : Halo, saya [REDACTED_PERSON] dengan nomor [REDACTED_PHONE] dan email [REDACTED_EMAIL]
```

The masked text is then safely passed to the AI agent.

---

## 📊 Performance & Monitoring

The system tracks:
- **CPU usage**
- **Memory usage**
- **NER API latency**

Metrics are collected using `psutil` and Python timing utilities, and can be logged or extended for observability tools.

---

## 🔐 Privacy & Safety Design

- Raw PII is **never sent** to the LLM
- Guardrail logic is **fully separated** from the AI agent
- NER service runs as an **independent microservice**
- Masking format preserves entity type for auditability

---

## 🚀 Use Cases

- AI Customer Service Systems
- Privacy-aware LLM Applications
- PII Guardrail for Chatbots
- Enterprise AI Compliance Scenarios

---

## 👤 Author

**Putra Syafiq**  
AI Engineer Internship – Take Home Test Project

---

## 📄 License

This project is intended for educational and evaluation purposes.
