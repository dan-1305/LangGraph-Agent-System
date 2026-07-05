
import sys
from pathlib import Path
import time
import codecs

# Ensure the root directory is in the system path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

# Force stdout to be UTF-8 for Windows console
if sys.stdout.encoding != 'utf-8':
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# --- CONFIGURATION ---
CHROMA_DB_CODE_DIR = BASE_DIR / "data" / "chroma_db_code"
# Number of relevant chunks to retrieve
K_RESULTS = 5

def query_codebase():
    """
    Initializes the RAG components and enters a loop to accept user queries.
    """
    print("--- 🧠 AI Self-Awareness Module: Codebase Query Tool ---")

    # 1. Check if the database directory exists
    if not CHROMA_DB_CODE_DIR.exists():
        print(f"❌ Error: Database directory not found at '{CHROMA_DB_CODE_DIR}'")
        print("   Please run 'tools/ingest_code.py' first to create the database.")
        return

    # 2. Initialize embeddings and vector store
    print("🧠 Loading vector database from disk...")
    try:
        start_time = time.time()
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma(
            persist_directory=str(CHROMA_DB_CODE_DIR), 
            embedding_function=embeddings
        )
        retriever = vectorstore.as_retriever(search_kwargs={"k": K_RESULTS})
        end_time = time.time()
        print(f"✅ Database loaded successfully in {end_time - start_time:.2f} seconds.")
    except Exception as e:
        print(f"❌ Critical Error: Failed to load ChromaDB. {e}")
        return

    # 3. Start query loop
    while True:
        try:
            question = input("\n❓ Enter your query about the codebase (or 'q' to quit): ")
            if question.lower() == 'q':
                break
            if not question.strip():
                continue

            # 4. Perform similarity search
            print("\n🔄 Searching for relevant code snippets...")
            start_time = time.time()
            docs = retriever.invoke(question)
            end_time = time.time()
            
            print(f"⚡️ Search completed in {end_time - start_time:.2f} seconds. Found {len(docs)} relevant chunks.")

            # 5. Display results
            if not docs:
                print("🤷 No relevant documents found in the codebase.")
                continue
            
            print("\n--- Top Relevant Code Snippets ---")
            for i, doc in enumerate(docs):
                source = doc.metadata.get("source", "Unknown file")
                content = doc.page_content
                
                print(f"\n--- Snippet {i+1}: (Source: {source}) ---")
                print(content)
                print("--------------------------------------" + "-" * len(source))

        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")

    print("\n👋 Exiting query tool. Goodbye!")

if __name__ == "__main__":
    query_codebase()
