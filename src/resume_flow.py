import argparse
import os
import sys
import json
import sqlite3
from pathlib import Path

# Bật mã hoá UTF-8 cho console Windows
import codecs
if sys.stdout.encoding != 'utf-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Setup Path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

def get_latest_checkpoint(db_path="circuit_breaker.db"):
    """Lấy Checkpoint state mới nhất từ SQLite"""
    if not os.path.exists(db_path):
        print(f"❌ Database {db_path} không tồn tại.")
        return None

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Lấy dòng cuối cùng dựa trên ID
        cursor.execute("SELECT id, timestamp, failed_node, state_dump FROM quota_exhaustion_logs ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()

        if row:
            log_id, timestamp, node, state_dump = row
            print(f"✅ Đã tìm thấy Checkpoint #{log_id} lúc {timestamp} tại Node: {node}")
            try:
                return json.loads(state_dump)
            except json.JSONDecodeError:
                print("⚠️ Lỗi: state_dump không phải JSON chuẩn. Cố gắng fallback...")
                # Nếu không thể parse, trả về dict rỗng để tránh crash hoàn toàn
                return {}
        else:
            print("ℹ️ Không có log Quota Exhaustion nào trong database.")
            return None
    except sqlite3.OperationalError as e:
        print(f"❌ Lỗi SQLite: {e}")
        return None

async def resume_graph(state: dict):
    from src.factory.main import build_meta_graph
    
    print("\n--- 🌟 SOVEREIGN RESURRECTION PROTOCOL ---")
    print("Biên dịch lại MetaGraph...")
    
    meta_graph = build_meta_graph()
    app = meta_graph.compile()

    # Xóa thông tin báo lỗi để hệ thống tiếp tục chạy thay vì bị chặn lại
    state.pop("error", None)
    
    # Ép buộc selected_workflow nếu đang là trạng thái lỗi
    if state.get("selected_workflow") in ["ROUTE_QUOTA_EXHAUSTED", "ROUTE_HALT"]:
        # Chuyển về trạng thái chờ quyết định lại
        state["selected_workflow"] = "" 
        
    print("\n🚀 Nạp lại State và khởi động đồ thị...")
    config = {"recursion_limit": 150}
    try:
        final_state = await app.ainvoke(state, config)
        print("\n--- META-GRAPH RUN COMPLETE (RESUMED)! ---")
    except Exception as e:
        print(f"\n❌ Lỗi khi Resume Graph: {e}")


def main():
    parser = argparse.ArgumentParser(description="Resume AI Factory Flow từ Checkpoint khi bị dính lỗi Rate Limit/Quota")
    parser.add_argument("--new-key", type=str, help="API Key mới để Hot-swap")
    parser.add_argument("--fallback-model", type=str, help="Chuyển model sang Model Fallback rẻ hơn (ví dụ: gemini-3.1-flash-lite)")
    args = parser.parse_args()

    # 1. Hot-Swap Cấu hình
    if args.new_key:
        os.environ["GCLI_API_KEY"] = args.new_key
        print("🔑 Đã thực hiện Hot-Swap API Key thành công!")
    
    # 2. Lấy Checkpoint
    state = get_latest_checkpoint()
    if not state:
        print("Tiến trình phục hồi kết thúc do không tìm thấy trạng thái hợp lệ.")
        return

    # Hot-swap Model trong State (nếu có lưu config model trong state, 
    # ở cấu trúc hiện tại ta đổi biến môi trường, hệ thống BaseAgent sẽ nạp lại)
    if args.fallback_model:
        os.environ["DEFAULT_MODEL"] = args.fallback_model
        print(f"🤖 Đã Hot-Swap Model thành công: {args.fallback_model}")

    # 3. Kích hoạt Async Resume
    import asyncio
    asyncio.run(resume_graph(state))


if __name__ == "__main__":
    main()
