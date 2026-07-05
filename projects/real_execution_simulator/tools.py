import subprocess
import os
import io
import sys
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from langchain_core.tools import tool

# Giải quyết lỗi encoding GBK trên Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# GUARDRAILS
ALLOWED_COMMAND_PREFIXES = ["uv run python", "pytest", "dir", "ls", "echo", ".venv\\Scripts\\python.exe", ".venv/Scripts/python"]
FORBIDDEN_COMMANDS = ["rm -rf", "git reset", "format", "format C:"]

@tool
def execute_terminal_command(command: str) -> Dict[str, Any]:
    """
    Thực thi một lệnh terminal trên hệ điều hành Windows và trả về kết quả.
    CHỈ dùng lệnh này để chạy script python (vd: `uv run python script.py`) hoặc chạy test.
    KHÔNG dùng để xóa file hay định dạng ổ cứng.
    """
    command = command.strip()
    
    # Kiểm tra an toàn cơ bản
    if any(forbidden in command.lower() for forbidden in FORBIDDEN_COMMANDS):
        return {"error": f"Lệnh bị chặn bởi Guardrail vì lý do an toàn: {command}", "exit_code": -1}
    
    if not any(command.startswith(prefix) for prefix in ALLOWED_COMMAND_PREFIXES):
        return {"error": f"Lệnh không được phép. Chỉ hỗ trợ các lệnh bắt đầu bằng: {ALLOWED_COMMAND_PREFIXES}", "exit_code": -1}

    print(f"\n[TERMINAL EXECUTION] Đang chạy lệnh: {command}")
    
    try:
        # Chạy lệnh
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=30 # Giới hạn 30s để tránh treo
        )
        
        # Cắt gọt output để tránh tràn token window
        stdout_text = result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout
        stderr_text = result.stderr[-2000:] if len(result.stderr) > 2000 else result.stderr
        
        return {
            "exit_code": result.returncode,
            "stdout": stdout_text,
            "stderr": stderr_text
        }
    except subprocess.TimeoutExpired:
        return {"error": "Lệnh chạy quá lâu (>30s) và đã bị ép dừng.", "exit_code": -1}
    except Exception as e:
        return {"error": str(e), "exit_code": -1}

@tool
def read_file_content(filepath: str) -> str:
    """
    Đọc nội dung của một file code.
    Sử dụng tool này khi nhận được error log để xem dòng code gây lỗi.
    """
    try:
        # Đảm bảo đường dẫn tuyệt đối từ root
        if not os.path.isabs(filepath):
            root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
            filepath = os.path.join(root_dir, filepath)
            
        if not os.path.exists(filepath):
            return f"Lỗi: Không tìm thấy file {filepath}"
            
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Thêm số dòng để dễ debug
        content_with_lines = "".join([f"{i+1:03d} | {line}" for i, line in enumerate(lines)])
        return content_with_lines
    except Exception as e:
        return f"Lỗi khi đọc file: {str(e)}"

@tool
def rewrite_entire_file(filepath: str, new_content: str) -> str:
    """
    Ghi đè toàn bộ nội dung mới vào một file. (Có cơ chế Backup tự động)
    Sử dụng tool này để sửa lỗi code sau khi đã đọc và phân tích xong.
    Chú ý: new_content phải là mã nguồn HOÀN CHỈNH, không được rút gọn.
    """
    try:
        import shutil
        if not os.path.isabs(filepath):
            root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
            filepath = os.path.join(root_dir, filepath)
            
        # Tự động backup file cũ trước khi ghi đè
        if os.path.exists(filepath):
            backup_path = filepath + ".bak"
            shutil.copy2(filepath, backup_path)
            print(f"[BACKUP] Đã sao lưu file gốc ra {backup_path}")
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return f"Thành công: Đã backup và ghi đè file {filepath}"
    except Exception as e:
        return f"Lỗi khi ghi file: {str(e)}"

@tool
def list_markdown_files(directory_path: str) -> str:
    """
    Quét một thư mục và trả về danh sách các file Markdown (.md).
    Sử dụng tool này khi CEO yêu cầu bạn đọc và tổng hợp tài liệu của dự án.
    """
    import glob
    try:
        if not os.path.isabs(directory_path):
            root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
            search_path = os.path.join(root_dir, directory_path, "**/*.md")
        else:
            search_path = os.path.join(directory_path, "**/*.md")
            
        md_files = glob.glob(search_path, recursive=True)
        if not md_files:
            return f"Không tìm thấy file .md nào trong {directory_path}"
            
        # Lấy đường dẫn tương đối để dễ đọc
        rel_files = []
        for file in md_files:
            try:
                rel_files.append(os.path.relpath(file, root_dir))
            except:
                rel_files.append(file)
                
        return "Danh sách file Markdown:\n" + "\n".join(rel_files)
    except Exception as e:
        return f"Lỗi khi quét thư mục: {str(e)}"

@tool
def restore_backup(filepath: str) -> str:
    """
    Phục hồi file từ bản backup (.bak). Dùng khi test file sau khi sửa bị lỗi nặng hơn.
    """
    try:
        import shutil
        if not os.path.isabs(filepath):
            root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
            filepath = os.path.join(root_dir, filepath)
            
        backup_path = filepath + ".bak"
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, filepath)
            return f"Thành công: Đã khôi phục file {filepath} từ bản backup."
        else:
            return f"Lỗi: Không tìm thấy bản backup {backup_path}."
    except Exception as e:
        return f"Lỗi khi khôi phục backup: {str(e)}"

# Tập hợp các tools để agent sử dụng
EXECUTION_TOOLS = [execute_terminal_command, read_file_content, rewrite_entire_file, restore_backup, list_markdown_files]
