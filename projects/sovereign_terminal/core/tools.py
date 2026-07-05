"""
Sovereign Terminal - Tools (Function Calling).
Định nghĩa các tool mà AI có thể gọi: read_file, write_file, run_command, list_files.
"""
import subprocess
import sys
from pathlib import Path
from .config import Config


def read_file(path: str) -> str:
    """Đọc nội dung file."""
    try:
        full_path = Config.ROOT_DIR / path if not Path(path).is_absolute() else Path(path)
        if not full_path.exists():
            return f"[ERROR] File không tồn tại: {path}"
        content = full_path.read_text(encoding="utf-8", errors="replace")
        # Giới hạn 5000 ký tự
        if len(content) > 5000:
            content = content[:5000] + f"\n... (cắt ngắn, tổng {len(content)} chars)"
        return content
    except Exception as e:
        return f"[ERROR] {e}"


def write_file(path: str, content: str) -> str:
    """Ghi nội dung vào file."""
    try:
        # Safety: Không ghi vào file bảo vệ
        filename = Path(path).name
        if filename in Config.PROTECTED_FILES:
            return f"[BLOCKED] File '{filename}' nằm trong danh sách bảo vệ. Không thể ghi."
        
        full_path = Config.ROOT_DIR / path if not Path(path).is_absolute() else Path(path)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")
        return f"[OK] Đã ghi {len(content)} ký tự vào {path}"
    except Exception as e:
        return f"[ERROR] {e}"


def run_command(command: str) -> str:
    """Chạy lệnh terminal."""
    try:
        # Safety: Kiểm tra lệnh nguy hiểm
        cmd_lower = command.lower().strip()
        for forbidden in Config.FORBIDDEN_COMMANDS:
            if forbidden.lower() in cmd_lower:
                return f"[BLOCKED] Lệnh chứa chuỗi nguy hiểm: '{forbidden}'"
        
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=Config.COMMAND_TIMEOUT,
            cwd=str(Config.ROOT_DIR),
        )
        output = result.stdout.strip()
        if result.returncode != 0 and result.stderr:
            output += f"\n[STDERR] {result.stderr.strip()}"
        # Giới hạn output
        if len(output) > 3000:
            output = output[:3000] + "\n... (cắt ngắn)"
        return output or "[OK] Lệnh hoàn thành (không có output)"
    except subprocess.TimeoutExpired:
        return f"[TIMEOUT] Lệnh chạy quá {Config.COMMAND_TIMEOUT}s"
    except Exception as e:
        return f"[ERROR] {e}"


def list_files(path: str = ".", recursive: bool = False) -> str:
    """Liệt kê files trong thư mục."""
    try:
        full_path = Config.ROOT_DIR / path if not Path(path).is_absolute() else Path(path)
        if not full_path.exists():
            return f"[ERROR] Đường dẫn không tồn tại: {path}"
        
        items = []
        if recursive:
            for item in sorted(full_path.rglob("*")):
                rel = item.relative_to(Config.ROOT_DIR)
                # Skip hidden dirs
                if not any(part.startswith('.') or part.startswith('__') for part in rel.parts[:-1]):
                    prefix = "📁" if item.is_dir() else "📄"
                    items.append(f"{prefix} {rel}")
        else:
            for item in sorted(full_path.iterdir()):
                prefix = "📁" if item.is_dir() else "📄"
                items.append(f"{prefix} {item.name}")
        
        return "\n".join(items[:100]) if items else "[EMPTY] Thư mục trống"
    except Exception as e:
        return f"[ERROR] {e}"


def trigger_factory_workflow(mode: str, project_name: str, requirement: str) -> str:
    """Kích hoạt LangGraph Factory Workflow (DevOps từ xa)."""
    try:
        import asyncio
        from src.factory.main import main as factory_main
        print(f"🏭 Đang kích hoạt Factory Workflow: {mode} - {project_name}")
        
        # Chạy workflow trong một event loop background hoặc đợi kết quả
        # Vì ta đang ở trong async context, nên ta có thể gọi nó trực tiếp nếu nó là async
        # Tuy nhiên execute_tool đang là synchronous.
        # Ta có thể dùng asyncio.run_coroutine_threadsafe nếu đang có loop
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Create a task to run it without blocking the terminal too much
            # But the user might want the result.
            task = loop.create_task(factory_main(mode=mode, project_name=project_name, user_requirement=requirement))
            return f"[OK] Đã kích hoạt LangGraph Factory (mode={mode}) chạy ngầm. Vui lòng xem log trong reports/."
        else:
            asyncio.run(factory_main(mode=mode, project_name=project_name, user_requirement=requirement))
            return f"[OK] Đã hoàn thành LangGraph Factory (mode={mode})."
    except Exception as e:
        return f"[ERROR] Lỗi kích hoạt Factory: {e}"


# --- Tool Schemas (OpenAI Function Calling format) ---
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Đọc nội dung của một file text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Đường dẫn file (tương đối từ root)"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Ghi nội dung vào file (tạo mới hoặc ghi đè).",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Đường dẫn file"},
                    "content": {"type": "string", "description": "Nội dung cần ghi"}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Chạy lệnh terminal/command line (có timeout 60s).",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Lệnh cần chạy (vd: 'dir', 'git status')"}
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Liệt kê file/thư mục trong một đường dẫn.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Đường dẫn thư mục (mặc định: root)"},
                    "recursive": {"type": "boolean", "description": "Liệt kê đệ quy (mặc định: false)"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "trigger_factory_workflow",
            "description": "Kích hoạt AI Factory (LangGraph) để tự động hóa viết code, review code hoặc vá lỗi (DevOps từ xa).",
            "parameters": {
                "type": "object",
                "properties": {
                    "mode": {"type": "string", "description": "Chế độ chạy (vd: 'new', 'qa_only', 'debate')"},
                    "project_name": {"type": "string", "description": "Tên dự án cần xử lý"},
                    "requirement": {"type": "string", "description": "Yêu cầu cho Factory (vd: 'Sửa lỗi file router.py')"}
                },
                "required": ["mode", "project_name", "requirement"]
            }
        }
    }
]

# Mapping tool name -> function
TOOL_MAP = {
    "read_file": read_file,
    "write_file": write_file,
    "run_command": run_command,
    "list_files": list_files,
    "trigger_factory_workflow": trigger_factory_workflow,
}


def execute_tool(name: str, arguments: dict) -> str:
    """Thực thi tool theo tên và trả về kết quả."""
    func = TOOL_MAP.get(name)
    if not func:
        return f"[ERROR] Tool '{name}' không tồn tại"
    
    try:
        return func(**arguments)
    except Exception as e:
        return f"[ERROR] Lỗi khi gọi {name}: {e}"