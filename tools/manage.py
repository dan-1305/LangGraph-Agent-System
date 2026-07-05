import os
import sys
import argparse
import subprocess
import codecs

if sys.stdout.encoding != 'utf-8':
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))

TOOL_MAP = {
    "system": {
        "clean": "system/system_cleaner.py",
        "qa": "system/batch_qa_runner.py",
        "update": "system/apply_updates.py",
        "roadmap": "system/generate_flagship_roadmap.py",
        "refactor": "system/refactor_architecture.py",
        "setup": "system/setup_project_foundation.py",
    },
    "rag": {
        "ingest": "rag_code/ingest_code.py",
        "query": "rag_code/query_code_db.py",
        "test": "rag_code/test_code_ingestion.py",
        "inspect": "rag_code/inspect_docs.py",
    },
    "scanners": {
        "freelance": "scanners/freelance_scanner.py",
        "internship": "scanners/internship_scanner.py",
    },
    "lorebook": {
        "ultimate_preset": "lorebook/create_ultimate_preset_v3.py",
        "delete_empty": "lorebook/delete_empty_docs.py",
        "find_empty": "lorebook/find_empty_docs.py",
        "merge_lorebook": "lorebook/merge_and_shorten_lorebook.py",
        "merge_physiology": "lorebook/merge_physiology_lorebook.py",
    },
    "comfy": {
        "cli": "comfy/clothoff_cli.py",
        "gui": "comfy/clothoff_gui.py",
        "hf_cli": "comfy/clothoff_hf_cli.py",
        "create_image": "comfy/create_clothoff_image.py",
    },
    "edtech": {
        "10_diem": "edtech/create_10_diem_docx.py",
        "bang_tra_cuu": "edtech/create_bang_tra_cuu_docx.py",
        "bmtt_cheatsheet": "edtech/create_bmtt_cheatsheet_docx.py",
        "bmtt_docx": "edtech/create_bmtt_docx.py",
        "full_10_cau": "edtech/create_full_10_cau_docx.py",
        "qtkdcks_rut_gon": "edtech/create_giai_de_cuong_qtkdcks_rut_gon.py",
        "qtkdcks_suy_luan": "edtech/create_giai_de_cuong_qtkdcks_suy_luan.py",
        "qtkdcks_giai": "edtech/create_giai_de_cuong_qtkdcks.py",
        "mindset": "edtech/create_mindset_docx.py",
        "audio_gtts": "edtech/create_qtkdcks_audio_gtts.py",
        "audio_local": "edtech/create_qtkdcks_audio_local.py",
        "audio_simple": "edtech/create_qtkdcks_audio_simple.py",
        "qtkdcks_cheatsheet": "edtech/create_qtkdcks_cheatsheet.py",
        "custom_audio": "edtech/create_qtkdcks_custom_audio.py",
        "qtkdcks_docx": "edtech/create_qtkdcks_docx.py",
        "theory_audio_story": "edtech/create_qtkdcks_theory_audio_story.py",
        "theory_audio": "edtech/create_qtkdcks_theory_audio.py",
        "quiz": "edtech/qtkdcks_decuong_quiz.py",
        "formula": "edtech/qtkdcks_formula_reflex.py",
        "quiz_app": "edtech/qtkdcks_quiz_app.py",
        "scan_pdfs": "edtech/scan_qtkdcks_pdfs.py",
        "verify_math": "edtech/verify_bmtt_math.py",
    },
    "misc": {
        "hentai_ocr": "misc/run_ocr_hentai.py"
    }
}

def print_help():
    print("==================================================")
    print("🚀 LANGGRAPH AGENT SYSTEM - CENTRAL TOOL MANAGER 🚀")
    print("==================================================")
    print("Sử dụng: python tools/manage.py <category> <command> [args...]")
    print("\\nDanh sách các công cụ có sẵn:")
    
    for category, commands in TOOL_MAP.items():
        print(f"\\n[{category.upper()}]")
        for cmd, script in commands.items():
            print(f"  {cmd:<20} -> Chạy {script}")
            
    print("\\nVí dụ:")
    print("  python tools/manage.py system clean --aggressive")
    print("  python tools/manage.py rag ingest")
    print("  python tools/manage.py edtech quiz_app")
    print("==================================================")

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help"]:
        print_help()
        sys.exit(0)
        
    category = sys.argv[1]
    if category not in TOOL_MAP:
        print(f"❌ Lỗi: Danh mục '{category}' không tồn tại.")
        print_help()
        sys.exit(1)
        
    if len(sys.argv) < 3:
        print(f"❌ Lỗi: Vui lòng chỉ định lệnh trong danh mục '{category}'.")
        print("Các lệnh có sẵn:")
        for cmd in TOOL_MAP[category]:
            print(f"  - {cmd}")
        sys.exit(1)
        
    command = sys.argv[2]
    if command not in TOOL_MAP[category]:
        print(f"❌ Lỗi: Lệnh '{command}' không tồn tại trong danh mục '{category}'.")
        sys.exit(1)
        
    script_path = os.path.join(TOOLS_DIR, TOOL_MAP[category][command])
    
    if not os.path.exists(script_path):
        print(f"❌ Lỗi: Không tìm thấy file script {script_path}")
        sys.exit(1)
        
    # Xây dựng lệnh gọi
    args = sys.argv[3:]
    cmd_run = [sys.executable, script_path] + args
    
    print(f"⚡ Đang khởi chạy: {' '.join(cmd_run)}\\n" + "-"*50)
    try:
        subprocess.run(cmd_run, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\\n❌ Lệnh thực thi kết thúc với mã lỗi {e.returncode}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\\n⏹️ Đã dừng do người dùng hủy.")
        
if __name__ == "__main__":
    main()
