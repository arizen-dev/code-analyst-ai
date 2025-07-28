---
title: AI Codebase Analyst
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: docker
app_file: app.py
pinned: false
---

# AI Codebase Analyst: Chat with any GitHub Repository

This project is an advanced AI agent capable of ingesting an entire public GitHub repository, performing a high-level architectural analysis, and then answering detailed technical questions about the code. It serves as a powerful tool for developers, accelerating code comprehension and onboarding.

This project showcases expertise in building complex, agentic AI systems that go beyond simple document Q&A to interact with file systems, parse structured code data, and provide valuable, context-aware insights for technical teams.

---

### 🚀 High-Level Workflow

The user provides a GitHub URL, and the system provides an instant architectural summary followed by an interactive Q&A session.

![User Workflow Diagram](diagrams/user-workflow.png)

---

### ✨ Features
- **GitHub Repository Ingestion:** Clones any public GitHub repository via its URL.
- **Automated Architectural Summary:** Provides an immediate high-level analysis of the project's purpose, tech stack, and key files.
- **Deep Code Q&A:** Leverages a RAG pipeline built on a vector store of the entire codebase.
- **Language-Aware Splitting:** Uses `langchain` and `tree-sitter` to intelligently chunk code files while preserving structure.
- **Modular & Professional Code Structure:** Organized into separate modules for UI, core logic, and prompts.
- **Safe Resource Management:** Automatically creates and cleans up temporary directories.

---

### 🛠️ Technical Architecture

The system uses a two-phase process: a one-time indexing pipeline to prepare the code, and an interactive Q&A pipeline for analysis.

![System Architecture Diagram](diagrams/system-architecture.png)

<details>
<summary>Click to see a detailed view of the RAG Q&A Pipeline</summary>

The core of the Q&A functionality is a Retrieval-Augmented Generation (RAG) pipeline. When a user asks a question, the system finds the most relevant code snippets from the vector store and provides them to the LLM as context to generate a precise, code-grounded answer.

![Detailed RAG Pipeline Diagram](diagrams/rag-pipeline.png)

</details>

---

### ⚙️ How to Run Locally

1.  **Prerequisite:** You must have `git` installed on your system.

2.  **Clone this repository:**
    ```bash
    git clone https://github.com/your-username/ai-code-analyst.git
    cd ai-code-analyst
    ```

3.  **Create a virtual environment and install dependencies:**
    ```bash
    # For Mac/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    # Install all required packages, including parsers
    pip install -r requirements.txt --upgrade
    ```

4.  **Set up your API Keys:**
    Create a file named `.env` in the project root. Add your keys for both OpenRouter and OpenAI:
    ```
    OPENROUTER_API_KEY="your_openrouter_api_key_here"
    OPENAI_API_KEY="your_openai_api_key_here"
    ```

5.  **Run the application:**
    ```bash
    chainlit run app.py -w
    ```
    Open your browser to `http://localhost:8000` to use the application.