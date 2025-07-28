# AI Codebase Analyst: Chat with any GitHub Repository

This project is an advanced AI agent that ingests public GitHub repositories, performs an architectural analysis, and answers detailed technical questions about the code to accelerate developer onboarding.

---

### 🎬 Video Walkthrough

Since this is a developer tool designed to be run locally, the best way to see it in action is to watch the video walkthrough.

[**WATCH THE 2-MINUTE VIDEO DEMO HERE**](https://www.loom.com/...)  <-- **IMPORTANT: Replace this with your real Loom or YouTube link.**

---

### ✨ Features
- **GitHub Repository Ingestion:** Clones any public GitHub repository via its URL.
- **Automated Architectural Summary:** Provides an immediate high-level analysis of the project's purpose, tech stack, and key files.
- **Deep Code Q&A:** Leverages a RAG pipeline to answer specific questions about the codebase.
- **Language-Aware Splitting:** Uses `langchain` and `tree-sitter` for intelligent, structure-preserving code chunking.
- **Modular & Professional Code Structure:** Demonstrates best practices by separating UI, core logic, and prompts.
- **Safe Resource Management:** Automatically creates and cleans up temporary directories for cloned repositories.

---

### 🛠️ Technical Architecture & Workflow

The system uses a two-phase process: a one-time indexing pipeline to prepare the code, and an interactive Q&A pipeline for analysis.

![User Workflow Diagram](diagrams/user-workflow.png)
![System Architecture Diagram](diagrams/system-architecture.png)

<details>
<summary>Click to see a detailed view of the RAG Q&A Pipeline</summary>

The core of the Q&A functionality is a Retrieval-Augmented Generation (RAG) pipeline. When a user asks a question, the system finds the most relevant code snippets from the vector store and provides them to the LLM as context to generate a precise, code-grounded answer.

![Detailed RAG Pipeline Diagram](diagrams/rag-pipeline.png)

</details>

---

### ⚙️ How to Run Locally

1.  **Prerequisites:** You must have `git` and `git-lfs` installed on your system.

2.  **Clone this repository:**
    ```bash
    git clone https://github.com/arizen-dev/code-analyst-ai.git
    cd code-analyst-ai
    ```

3.  **Create a virtual environment and install dependencies:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Install all required packages
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