import os
import sys
from pathlib import Path
import uuid
import asyncio

# Thêm root path để import
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.factory.graph import build_factory_graph

def get_all_projects(projects_dir: Path):
    projects = []
    if not projects_dir.exists():
        return projects
    for item in projects_dir.iterdir():
        if item.is_dir() and not item.name.startswith("_") and item.name not in ["data"]:
            projects.append(item.name)
    return projects

def main():
    print("==================================================")
    print("🚀 BATCH QA RUNNER - NÂNG ĐIỂM HÀNG LOẠT LÊN 8.0+")
    print("==================================================")
    
    projects_dir = Path(__file__).resolve().parent.parent.parent / "projects"
    projects = get_all_projects(projects_dir)
    
    if not projects:
        print("Không tìm thấy dự án nào trong thư mục projects/")
        return
        
    print(f"Danh sách các dự án sẽ được quét: {', '.join(projects)}\n")
    
    graph = build_factory_graph()
    results = {}
    
    for project_name in projects:
        print(f"\n" + "="*50)
        print(f"🔍 BẮT ĐẦU QA CHO DỰ ÁN: {project_name}")
        print("="*50)
        
        initial_state = {
            "request_id": str(uuid.uuid4()),
            "project_name": project_name,
            "project_path": f"projects/{project_name}",
            "user_requirement": "",
            "mode": "qa_only",
            "revision_count": 0
        }
        
        try:
            # Bắt buộc tạo event loop để chạy ainvoke
            final_state = asyncio.run(graph.ainvoke(initial_state))
            score = final_state.get('qa_score', 0)
            results[project_name] = score
            print(f"\n🎉 HOÀN TẤT QA CHO DỰ ÁN {project_name} | ĐIỂM CUỐI: {score}/10")
        except Exception as e:
            print(f"\n❌ DỰ ÁN {project_name} GẶP LỖI: {e}")
            results[project_name] = "Lỗi"
            
    print("\n" + "="*50)
    print("📊 BẢNG TỔNG HỢP KẾT QUẢ BATCH QA:")
    for proj, score in results.items():
        print(f" - {proj}: {score}")
    print("="*50)

if __name__ == "__main__":
    main()
