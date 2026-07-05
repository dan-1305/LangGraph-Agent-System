
import os
from pathlib import Path
import sys

# Ensure the root directory is in the system path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from typing import List

# --- CONFIGURATION ---
# The root directory of the codebase to ingest
CODE_ROOT = BASE_DIR
# The directory to store the new ChromaDB instance for code
CHROMA_DB_CODE_DIR = BASE_DIR / "data" / "chroma_db_code"
# File extensions to include in the ingestion
INCLUDED_EXTENSIONS = {".py", ".md", ".json", ".txt", ".in"}
# Directories to exclude from ingestion
EXCLUDED_DIRS = {
    ".venv",
    ".git",
    "__pycache__",
    "node_modules",
    "build",
    "dist",
    "reports",
    "logs",
    "data", # Exclude the data directory itself to avoid ingesting databases or large files
}

def get_all_code_files(root_dir: Path) -> List[Path]:
    """
    Scans the directory tree and returns a list of file paths to be ingested.
    """
    code_files = []
    for root, dirs, files in os.walk(root_dir):
        # Modify the dir list in-place to prevent os.walk from descending into excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix in INCLUDED_EXTENSIONS:
                code_files.append(file_path)
    return code_files

def ingest_codebase():
    """
    Main function to orchestrate the codebase ingestion process.
    """
    print("--- AI Self-Awareness Module: Codebase Ingestion ---")
    
    # 1. Scan for files
    print(f"Scanning for code files in: {CODE_ROOT}")
    files_to_ingest = get_all_code_files(CODE_ROOT)
    print(f"Found {len(files_to_ingest)} files to ingest.")

    if not files_to_ingest:
        print("No files found. Exiting.")
        return

    # 2. Load documents
    print("Loading document contents...")
    all_docs = []
    for file_path in files_to_ingest:
        try:
            loader = TextLoader(str(file_path), encoding="utf-8")
            docs = loader.load()
            # Add file path as metadata to each document
            for doc in docs:
                doc.metadata["source"] = str(file_path.relative_to(CODE_ROOT))
            all_docs.extend(docs)
        except Exception as e:
            print(f"Could not load file {file_path}: {e}")
            continue
    
    print(f"Loaded {len(all_docs)} documents.")

    # 3. Split documents into chunks
    print("Splitting documents into manageable chunks...")
    # Using a text splitter designed for code
    text_splitter = RecursiveCharacterTextSplitter.from_language(
        language="python", chunk_size=2000, chunk_overlap=200
    )
    chunks = text_splitter.split_documents(all_docs)
    print(f"Split into {len(chunks)} chunks.")

    # 4. Create embeddings and store in ChromaDB
    print("Creating embeddings and persisting to ChromaDB...")
    print(f"   (This may take a while depending on the number of chunks...)")
    
    # Using a lightweight, effective model for local CPU
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Create the vector store and persist it
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DB_CODE_DIR)
    )
    
    print("\n--- INGESTION COMPLETE ---")
    print(f"VectorDB for codebase created successfully at: {CHROMA_DB_CODE_DIR}")
    print("The AI is now one step closer to self-awareness.")

if __name__ == "__main__":
    ingest_codebase()
