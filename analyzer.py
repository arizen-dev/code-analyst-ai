# analyzer.py
import os
import tempfile
import shutil
import subprocess
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough

from prompts import INITIAL_ANALYSIS_PROMPT, RAG_PROMPT_TEMPLATE

class GitHubRepoAnalyzer:
    def __init__(self, model_name="anthropic/claude-3.5-sonnet"):
        self.temp_dir = tempfile.mkdtemp()
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.1,
            streaming=True,
            api_key=os.environ.get("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )
        
        # --- BATCHING FIX APPLIED ---
        # Added `chunk_size` to process documents in smaller batches,
        # preventing API token limit errors.
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            chunk_size=200  # Process 200 documents per API call
        )
        
        self.retriever = None

    def clone_repo(self, repo_url: str):
        """Clones a public GitHub repository into the temporary directory."""
        try:
            subprocess.run(["git", "clone", repo_url, self.temp_dir], check=True, capture_output=True, text=True)
            return True, "Repository cloned successfully."
        except subprocess.CalledProcessError as e:
            error_message = f"Failed to clone repository. Error: {e.stderr}"
            self.cleanup()
            return False, error_message

    def load_and_index_files(self):
        """Loads code, splits it, and creates a FAISS vector store."""
        loader = GenericLoader.from_filesystem(
            self.temp_dir,
            glob="**/*",
            suffixes=[".py", ".js", ".ts", ".md", ".java", ".go", ".rs", ".html", ".css", "Dockerfile"],
            exclude=["**/.*", "**/__pycache__/**", "**/node_modules/**"],
            parser=LanguageParser(),
        )
        docs = loader.load()
        
        splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.PYTHON, chunk_size=2000, chunk_overlap=200
        )
        texts = splitter.split_documents(docs)
        
        # This will now make multiple, smaller API calls behind the scenes
        vector_store = FAISS.from_documents(texts, self.embeddings)
        self.retriever = vector_store.as_retriever()

    def _get_file_structure(self):
        """Generates a string representation of the file structure."""
        file_structure = ""
        for root, dirs, files in os.walk(self.temp_dir):
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'venv', '__pycache__', '.vscode', '.idea']]
            level = root.replace(self.temp_dir, '').count(os.sep)
            indent = ' ' * 4 * level
            file_structure += f"{indent}{os.path.basename(root)}/\n"
            sub_indent = ' ' * 4 * (level + 1)
            for f in files:
                file_structure += f"{sub_indent}{f}\n"
        return file_structure

    async def get_initial_analysis(self):
        """Performs a high-level analysis based on file structure and README."""
        file_structure = self._get_file_structure()
        readme_path = os.path.join(self.temp_dir, "README.md")
        readme_content = "No README.md file found."
        if os.path.exists(readme_path):
            with open(readme_path, "r", encoding="utf-8", errors="ignore") as f:
                readme_content = f.read()

        analysis_prompt = ChatPromptTemplate.from_template(INITIAL_ANALYSIS_PROMPT)
        analysis_chain = analysis_prompt | self.llm
        
        response = await analysis_chain.ainvoke({
            "file_structure": file_structure,
            "readme_content": readme_content
        })
        return response.content

    def get_rag_chain(self):
        """Creates and returns the RAG chain for Q&A."""
        rag_prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
        return (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | rag_prompt
            | self.llm
        )

    def cleanup(self):
        """Deletes the temporary directory, ignoring errors."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)