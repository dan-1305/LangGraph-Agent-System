import os
import shutil
import sys
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

# Base Path Resolution & Environment Initialization
BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(BASE_DIR / ".env")

from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import pymupdf4llm

# Pipeline Directory Constants
storage_dir = os.getenv("STORAGE_DIR")
base_data_dir = Path(storage_dir) if storage_dir else BASE_DIR / "data"

PENDING_DIR: Path = base_data_dir / "document" / "01_Pending_Ingestion"
INGESTED_DIR: Path = base_data_dir / "document" / "02_Ingested_Active_Brain"
NOISE_DIR: Path = base_data_dir / "document" / "03_Archived_Noise"
CHROMA_DB_DIR: Path = base_data_dir / "knowledge_db"


def bootstrap_environment() -> None:
    """Khởi tạo toàn bộ hạ tầng thư mục lưu trữ nếu chưa tồn tại."""
    for directory in [PENDING_DIR, INGESTED_DIR, NOISE_DIR]:
        directory.mkdir(parents=True, exist_ok=True)


def collect_pending_assets(target_dir: Path) -> List[Path]:
    """Quét và thu thập danh sách các tập tin PDF đang chờ xử lý."""
    return list(target_dir.glob("*.pdf"))


def parse_pdf_to_markdown_and_chunk(
    pdf_files: List[Path], chunk_size: int, chunk_overlap: int
) -> List[Document]:
    """Trích xuất PDF bằng PyMuPDF4LLM, băm theo Markdown và Recursive."""
    all_chunks: List[Document] = []
    
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    md_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    
    char_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )

    for pdf_file in pdf_files:
        print(f"📖 Đang xử lý: {pdf_file.name}...")
        try:
            md_text = pymupdf4llm.to_markdown(str(pdf_file))
            md_docs = md_splitter.split_text(md_text)
            
            for doc in md_docs:
                doc.metadata["source"] = pdf_file.name
                
            chunks = char_splitter.split_documents(md_docs)
            all_chunks.extend(chunks)
            print(f"   -> Tạo được {len(chunks)} chunks.")
        except Exception as e:
            print(f"   ⚠️ Lỗi khi xử lý file {pdf_file.name}: {e}")
            
    return all_chunks


def safe_initialize_embeddings() -> HuggingFaceEmbeddings:
    """Khởi tạo mô hình Embedding cục bộ. Tích hợp cơ chế Fallback."""
    primary_model: str = os.getenv("PRIMARY_EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    fallback_model: str = os.getenv("FALLBACK_EMBEDDING_MODEL", "paraphrase-MiniLM-L3-v2")
    
    try:
        print(f"🧠 Đang nạp mô hình Embedding tối ưu: {primary_model}")
        return HuggingFaceEmbeddings(model_name=primary_model)
    except (RuntimeError, Exception) as error:
        print(f"⚠️ Cảnh báo tài nguyên/Kết nối: Lỗi nạp mô hình chính ({error}).")
        print(f"🔄 Kích hoạt cơ chế phòng vệ: Chuyển sang mô hình dự phòng nhẹ: {fallback_model}")
        return HuggingFaceEmbeddings(model_name=fallback_model)


def commit_to_vectorstore(
    chunks: List[Document], embeddings: HuggingFaceEmbeddings, db_path: Path
) -> Optional[Chroma]:
    """Lưu trữ các vector dữ liệu vào hệ quản trị cơ sở dữ liệu vector ChromaDB."""
    try:
        return Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=str(db_path)
        )
    except Exception as error:
        print(f"❌ Khóa giới hạn/Lỗi IO: Không thể ghi dữ liệu vào ChromaDB. Chi tiết: {error}")
        return None


def relocate_processed_assets(source_files: List[Path], destination_dir: Path) -> None:
    """Di chuyển các tệp tin gốc đã xử lý thành công sang phân vùng lưu trữ lâu dài."""
    print("📦 Đang tiến hành lưu kho và phân loại các tệp tin gốc...")
    for file_path in source_files:
        try:
            target_path: Path = destination_dir / file_path.name
            if target_path.exists():
                target_path.unlink()
            shutil.move(str(file_path), str(target_path))
            print(f"   -> Đã dời: {file_path.name}")
        except OSError as error:
            print(f"   ⚠️ Thất bại khi di chuyển tệp {file_path.name}: {error}")


def run_pipeline() -> None:
    """Hàm điều phối (Orchestrator) thực thi toàn bộ chu trình nạp dữ liệu."""
    bootstrap_environment()
    
    print(f"🔄 Đang đọc các file PDF từ {PENDING_DIR} (Sử dụng PyMuPDF4LLM)...")
    pdf_assets: List[Path] = collect_pending_assets(PENDING_DIR)
    
    if not pdf_assets:
        print("⚡ Thư mục Pending trống. Không phát hiện tài liệu mới để nạp.")
        return

    print(f"🔄 Bắt đầu xử lý {len(pdf_assets)} tài liệu khoa học...")

    chunk_size: int = int(os.getenv("CHUNK_SIZE", 1200))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", 150))

    processed_chunks: List[Document] = parse_pdf_to_markdown_and_chunk(
        pdf_assets, chunk_size, chunk_overlap
    )
    
    if not processed_chunks:
        print("❌ Không tạo được chunk nào. Thoát.")
        return

    print(f"✅ Hoàn tất băm nhỏ dữ liệu thành {len(processed_chunks)} chunks.")

    embedding_engine: HuggingFaceEmbeddings = safe_initialize_embeddings()
    
    db_instance: Optional[Chroma] = commit_to_vectorstore(
        processed_chunks, embedding_engine, CHROMA_DB_DIR
    )

    if db_instance is not None:
        relocate_processed_assets(pdf_assets, INGESTED_DIR)
        print(f"🎉 Hệ thống RAG đã được cập nhật thành công tại: {CHROMA_DB_DIR}")
    else:
        print("❌ Tiến trình Ingest thất bại nghiêm trọng tại bước ghi DB. Giữ nguyên tệp để bảo toàn dữ liệu.")


if __name__ == "__main__":
    if sys.platform == "win32" and hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    run_pipeline()
