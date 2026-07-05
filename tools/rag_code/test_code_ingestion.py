
import sys
from pathlib import Path
import time
import io

# Ensure the root directory is in the system path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# --- CONFIGURATION ---
CHROMA_DB_CODE_DIR = BASE_DIR / "data" / "chroma_db_code"
REPORT_FILE = BASE_DIR / "reports" / "code_ingestion_report.md"
K_RESULTS = 5  # Number of relevant chunks to retrieve

# --- TEST QUERIES ---
TEST_QUERIES = [
    {
        "id": "Accuracy Test",
        "question": "Hàm nào chịu trách nhiệm fetch dữ liệu từ Binance?",
        "expected_source": "projects/ai_trading_agent/src/binance_executor.py"
    },
    {
        "id": "Logic Comprehension Test",
        "question": "Giải thích cách hệ thống ai_trading_agent xử lý rủi ro.",
        "expected_source": "projects/ai_trading_agent/src/langgraph_agent.py"
    },
    {
        "id": "Config Location Test",
        "question": "Where is the InfluxDB configuration located?",
        "expected_source": "projects/ai_trading_agent/src/config.py"
    }
]

def run_automated_tests():
    """
    Runs a predefined set of queries against the codebase vector database
    and generates a markdown report.
    """
    print("--- Automated Codebase Ingestion Test ---")

    # 1. Check for DB
    if not CHROMA_DB_CODE_DIR.exists():
        print(f"Error: Database directory not found at '{CHROMA_DB_CODE_DIR}'")
        print("   Please run 'tools/ingest_code.py' first.")
        return

    # 2. Load DB
    print("Loading vector database from disk...")
    try:
        start_time = time.time()
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma(
            persist_directory=str(CHROMA_DB_CODE_DIR), 
            embedding_function=embeddings
        )
        retriever = vectorstore.as_retriever(search_kwargs={"k": K_RESULTS})
        load_time = time.time() - start_time
        print(f"Database loaded in {load_time:.2f} seconds.")
    except Exception as e:
        print(f"Critical Error: Failed to load ChromaDB. {e}")
        return

    # 3. Run tests and capture output
    report_content = io.StringIO()
    report_content.write("# Code Ingestion & Retrieval Test Report\n\n")
    report_content.write(f"**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    report_content.write(f"**Database Load Time:** {load_time:.2f} seconds\n\n")
    report_content.write("---\n")

    overall_success = True

    for test in TEST_QUERIES:
        print(f"\nRunning Test: {test['id']}...")
        report_content.write(f"\n## Test Case: {test['id']}\n\n")
        report_content.write(f"**Query:** `{test['question']}`\n\n")

        start_time = time.time()
        docs = retriever.invoke(test['question'])
        query_time = time.time() - start_time
        
        report_content.write(f"**Performance:** Query completed in **{query_time:.2f} seconds**.\n\n")
        
        if not docs:
            report_content.write("**Result:** No relevant documents found.\n")
            report_content.write("**Analysis:** <font color='red'>FAIL</font> - The database failed to retrieve any results.\n")
            overall_success = False
            continue

        report_content.write("### Top Retrieved Snippets:\n\n")
        
        found_expected_source = False
        for i, doc in enumerate(docs):
            source = doc.metadata.get("source", "Unknown file")
            content = doc.page_content
            
            # Check if this snippet is from the expected source
            if test['expected_source'] in source:
                found_expected_source = True
            
            report_content.write(f"#### Snippet {i+1} (Source: `{source}`)\n")
            report_content.write("```python\n")
            report_content.write(content + "\n")
            report_content.write("```\n")

        # Analysis
        report_content.write("\n**Analysis:** ")
        if found_expected_source:
            report_content.write(f"<font color='green'>PASS</font> - The retrieved snippets include the expected source file (`{test['expected_source']}`). This indicates good relevance.\n")
        else:
            report_content.write(f"<font color='orange'>WARN</font> - The top {K_RESULTS} results did not contain the expected source file (`{test['expected_source']}`). The retrieval might not be optimally tuned.\n")
            overall_success = False # Consider a warning as a failure for strict testing
            
        report_content.write("---\n")

    # Final Summary
    print("\n--- All Tests Completed ---")
    report_content.write("\n## Summary\n\n")
    if overall_success:
        report_content.write("Overall, the codebase ingestion and retrieval system is **functional and effective**. The queries returned relevant results from the expected source files within an acceptable time frame.\n")
    else:
        report_content.write("The system is **partially functional**, but improvements are needed. Some queries did not return snippets from the most relevant source files, suggesting that chunking strategy or retrieval parameters could be optimized.\n")

    # 4. Write report to file
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report_content.getvalue())
        
    print(f"Report saved to: {REPORT_FILE}")

if __name__ == "__main__":
    run_automated_tests()
