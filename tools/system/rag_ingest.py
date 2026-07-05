import os
import sys
import json
import hashlib
import chromadb
import argparse
import psutil
from pathlib import Path
from dotenv import load_dotenv

# Nạp biến môi trường từ .env (để lấy cấu hình HF_HOME)
root_dir = Path(__file__).resolve().parent.parent.parent
load_dotenv(root_dir / '.env')

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import MarkdownHeaderTextSplitter

# Đảm bảo in console tiếng Việt không lỗi trên Windows
if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

def get_file_hash(file_path: Path) -> str:
    """Tính mã băm MD5 của một file."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def load_hash_cache(cache_file: Path) -> dict:
    if cache_file.exists():
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_hash_cache(cache_file: Path, cache_data: dict):
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=4)

def check_resource_guard():
    """Kiểm tra xem hệ thống còn đủ RAM để chạy tác vụ nặng không."""
    mem = psutil.virtual_memory()
    free_gb = mem.available / (1024**3)
    print(f"📊 Kiểm tra tài nguyên: RAM trống {free_gb:.2f} GB")
    
    # Ngưỡng an toàn: Ít nhất 1.0GB RAM trống để load model Embedding siêu nhẹ
    if free_gb < 1.0:
        print("❌ [RESOURCE GUARD] CẢNH BÁO: RAM trống quá thấp (< 1.0GB).")
        print("   Để tránh treo máy, quá trình Ingest bị chặn.")
        print("   Vui lòng tắt bớt ứng dụng rồi thử lại.")
        return False
    return True

def main(force_all=False):
    # Kích hoạt Resource Guard
    if not check_resource_guard():
        sys.exit(1)

    root_dir = Path(__file__).resolve().parent.parent.parent
    context_dir = root_dir / 'context'
    docs_dir = root_dir / 'docs'
    
    storage_dir = os.getenv("STORAGE_DIR")
    base_data_dir = Path(storage_dir) if storage_dir else root_dir / 'data'
    
    db_path = base_data_dir / 'chroma_db'
    cache_path = base_data_dir / 'rag_file_cache.json'
    
    # Tạo thư mục chứa db nếu chưa có
    db_path.parent.mkdir(exist_ok=True)
    
    print("🚀 Bắt đầu Ingest tài liệu vào ChromaDB...")
    print(f"Thư mục DB: {db_path}")
    
    # 1. Khởi tạo Chroma Client và Collection
    client = chromadb.PersistentClient(path=str(db_path))
    
    # Lấy hoặc tạo collection
    try:
        collection = client.get_collection(name="system_architecture_docs")
    except Exception:
        collection = client.create_collection(name="system_architecture_docs")
        force_all = True # Force rebuild nếu collection chưa tồn tại
        
    if force_all:
        try:
            client.delete_collection("system_architecture_docs")
            print("Đã xóa collection cũ để làm mới toàn bộ.")
            collection = client.create_collection(name="system_architecture_docs")
        except Exception:
            pass
            
    hash_cache = load_hash_cache(cache_path) if not force_all else {}
    new_hash_cache = {}
    
    # 2. Cấu hình Hierarchical Text Splitter (Chia nhỏ markdown chuẩn RAG Enterprise)
    # Tách đoạn một cách trọn vẹn theo các thẻ Header của Markdown
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    
    # 3. Quét các file .md
    files_to_ingest = []
    
    # Lấy tất cả file .md trong thư mục context
    if context_dir.exists():
        files_to_ingest.extend(list(context_dir.glob('**/*.md')))
    
    # Lấy tất cả file .md trong thư mục docs
    if docs_dir.exists():
        files_to_ingest.extend(list(docs_dir.glob('**/*.md')))
        
    print(f"Tìm thấy {len(files_to_ingest)} files Markdown.")
    
    all_chunks = []
    all_metadatas = []
    all_ids = []
    files_processed = 0
    
    for file_path in files_to_ingest:
        rel_path = str(file_path.relative_to(root_dir))
        current_hash = get_file_hash(file_path)
        new_hash_cache[rel_path] = current_hash
        
        # Bỏ qua nếu file không thay đổi (Incremental Ingestion)
        if not force_all and hash_cache.get(rel_path) == current_hash:
            continue
            
        files_processed += 1
        
        try:
            # Xóa các chunk cũ của file này trong DB trước khi nạp lại
            try:
                collection.delete(where={"source": rel_path})
            except Exception:
                pass
                
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Hierarchical Chunking
            chunks = splitter.split_text(content)
            
            for i, chunk in enumerate(chunks):
                # Bỏ qua các chunk quá nhỏ (rác)
                if len(chunk.page_content.strip()) < 50:
                    continue
                    
                all_chunks.append(chunk.page_content)
                
                # Trích xuất Header thành metadata (nếu có)
                chunk_headers = chunk.metadata
                header_context = " | ".join(f"{k}: {v}" for k, v in chunk_headers.items())
                
                # Lưu metadata chuẩn
                rel_path = str(file_path.relative_to(root_dir))
                parts = Path(rel_path).parts
                domain = parts[0]
                if domain == "projects" and len(parts) > 1:
                    domain = parts[1]
                    
                meta = {
                    "source": rel_path,
                    "domain": domain,
                    "chunk_index": i,
                    "headers": header_context
                }
                all_metadatas.append(meta)
                all_ids.append(f"{rel_path}_chunk_{i}")
                
            print(f"Đã xử lý mới/cập nhật: {file_path.name} ({len(chunks)} chunks)")
        except Exception as e:
            print(f"Lỗi khi xử lý file {file_path}: {e}")
            
    if not all_chunks:
        print("\n⚡ Không có file nào thay đổi. Bỏ qua quá trình nhúng (Saved CPU/RAM).")
        save_hash_cache(cache_path, new_hash_cache)
        return
            
    # Load model embedding (chỉ load khi có data cần nhúng để tiết kiệm RAM)
    # [TỐI ƯU HÓA] Sử dụng model MiniLM siêu nhẹ (1GB RAM) thay cho bge-m3 (7GB RAM)
    print("\nĐang tải model Embedding siêu nhẹ (all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # 4. Nhúng vào ChromaDB (Chia batch nhỏ để tránh Memory Error)
    print(f"Bắt đầu nhúng {len(all_chunks)} chunks vào VectorDB...")
    
    batch_size = 50
    for i in range(0, len(all_chunks), batch_size):
        batch_chunks = all_chunks[i:i+batch_size]
        batch_metadatas = all_metadatas[i:i+batch_size]
        batch_ids = all_ids[i:i+batch_size]
        
        # Tạo vector
        batch_embeddings = embeddings.embed_documents(batch_chunks)
        
        # Lưu vào Chroma
        collection.add(
            embeddings=batch_embeddings,
            documents=batch_chunks,
            metadatas=batch_metadatas,
            ids=batch_ids
        )
        print(f"  Đã nhúng batch {i//batch_size + 1}/{(len(all_chunks)-1)//batch_size + 1}")
        
    save_hash_cache(cache_path, new_hash_cache)
    print(f"✅ HOÀN TẤT! Đã cập nhật {files_processed} file vào VectorDB.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Force rebuild toàn bộ database")
    args = parser.parse_args()
    main(force_all=args.force)
