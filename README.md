# Veterinary RAG Chatbot

A conversational veterinary support chatbot for dairy cattle health management.

The system supports:

* domain-specific veterinary question answering
* context-aware follow-up handling
* vague query rewriting
* false-positive prevention during retrieval
* persistent chat memory
* conversational smalltalk handling
* frontend-backend integration

---

# Features

* RAG-based veterinary QA system
* LangGraph workflow orchestration
* Context-aware follow-up understanding
* Query rewriting for vague prompts
* Retrieval validation and false-positive prevention
* Persistent conversation memory
* Smalltalk/greeting handling
* FastAPI backend
* HTML/CSS/JavaScript frontend
* OpenAI API integration
* Modular backend architecture

---

# Architecture

```text
Frontend (HTML/CSS/JS)
        ↓
FastAPI Backend
        ↓
LangGraph Workflow
        ↓
RAG Retrieval + OpenAI LLM
        ↓
Persistent Memory
```

---

# LangGraph Workflow

```text
START
  ↓
detect_smalltalk
  ↓
route_initial
   ├── smalltalk_response
   └── retrieve_raw
            ↓
       detect_vague
            ↓
       route_after_raw
            ├── generate
            ├── rewrite
            └── fallback

rewrite
   ↓
route_after_rewrite
   ├── generate
   └── fallback
```

---

# Design Decisions

## Query Rewriting

The chatbot supports vague follow-up prompts such as:

* "explain again"
* "what about symptoms"
* "tell me more"

A rewrite step converts these into standalone queries using conversation history.

Example:

```text
User: What is mastitis?
User: Explain again

Rewritten Query:
Explain mastitis again
```

---

## False-Positive Prevention

A major challenge in conversational RAG systems is history takeover.

Example problem:

```text
User: What is mastitis?
User: What is pneumonia?
```

A naive rewrite system may incorrectly rewrite the second query into something mastitis-related because of previous history.

To prevent this:

* raw retrieval is checked first
* rewriting is only attempted for vague queries
* rewritten retrieval must pass relevance thresholds
* rewritten retrieval must outperform the original query retrieval

This prevents unrelated questions from being incorrectly forced into previous conversation context.

---

## Smalltalk Routing

Pleasantries such as:

* hello
* thanks
* bye

are routed separately from the RAG pipeline.

This prevents unnecessary retrieval/rewrite operations and avoids conversational queries being incorrectly tied to veterinary knowledge.

---

## Why LangGraph

LangGraph was used to:

* modularize routing logic
* separate decision nodes from processing nodes
* improve workflow readability
* support future extensibility
* make tool integration easier in future versions

---

# Tech Stack

## Backend

* Python
* FastAPI
* LangGraph
* Sentence Transformers
* OpenAI API
* ChromaDB

## Frontend

* HTML
* CSS
* Vanilla JavaScript

---

# Project Structure

```text
backend/
│
├── graph/
│   ├── builder.py
│   ├── states.py
│   ├── nodes/
│   └── routes/
│
├── routes/
│   ├── chat.py
│   └── login.py
│
├── services/
│   ├── rag.py
│   ├── llm.py
│   ├── rewrite.py
│   ├── memory.py
│   └── smalltalk.py
│
│
└── main.py

data/
|
├── knowledge_base/
|   └── kb.txt
|
└── users/
    └── <phone_number>.json


frontend/
│
├── login.html
├── chat.html
│
├── css/
│   └── style.css
│
└── js/
    ├── login.js
    └── chat.js
README.md
requirements.txt
.env.example
```

---

# Setup Instructions

## 1. Extract the Project folder

Extract the provided ZIP file and open the project folder in a terminal or code editor.

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Requirements

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY="your_api_key_here"
```

---

# Running the Backend

From project root:

```bash
uvicorn backend.main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

---

# Running the Frontend

Open a new terminal.

```bash
cd frontend
python -m http.server 5500
```

Frontend runs at:

```text
http://localhost:5500/login.html
```

Open Frontend (http://localhost:5500/login.html) in browser.

---

# Example Queries

* Hello
* What is mastitis?
* Explain further
* How to prevent FMD?
* Tell me more
* How does it present?
* How does pneumonia present in cattle?
* Thank you

---

# API Endpoints

## POST /login

Registers/loads a user session.

### Request

```json
{
  "phone": "9876543210"
}
```

---

## POST /chat

Processes a user query.

### Request

```json
{
  "phone": "9876543210",
  "message": "What is mastitis?"
}
```

### Response

```json
{
  "response": "Mastitis is an udder infection..."
}
```

---

## GET /history/{phone}

Loads previous chat history.

---

# Current Limitations

* Single-chat interface
* No authentication system
* Small domain-specific knowledge base
* Local storage used for frontend session persistence

---

# Future Improvements

* Multi-chat support
* Tool integration (weather/veterinary APIs)
* Streaming LLM responses
* Authentication and user accounts
* Deployment to cloud platforms
* Larger veterinary knowledge base
* Admin dashboard for monitoring
* Voice-based interaction

---

# Notes

The project was initially developed using local LLM inference through Ollama. During later development and testing phases, the OpenAI API was integrated to improve inference speed and iteration efficiency while preserving the same overall architecture.

The system remains model-agnostic and can be adapted back to local models with minimal changes.
