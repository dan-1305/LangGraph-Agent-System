"""
Sovereign Terminal - Persona Loader.
Nạp System Prompt từ .clinerules, GLOBAL_STATE, và ACTIVE_THOUGHTS.
"""
from pathlib import Path
from .config import Config


def load_persona() -> str:
    """
    Load System Prompt đồ sộ từ các file cốt lõi của hệ thống.
    Giúp Agent có 100% trí nhớ và tính cách của CEO Sovereign.
    """
    root = Config.ROOT_DIR
    parts = []
    
    # 1. Base Identity
    parts.append("""Bạn là CEO Sovereign - Kiến trúc sư trưởng và Người điều phối tối cao của Hệ sinh thái LangGraph Agent System.
Bạn đang chạy ở chế độ HEADLESS (không cần Cline/VSCode). Bạn có đầy đủ quyền năng đọc/ghi file và chạy terminal.

NGUYÊN TẮC TỐI THƯỢNG:
1. In ra [ACTIVE ROLE: <Role Name>] ở đầu mỗi phản hồi.
2. Tuân thủ tuyệt đối Hiến pháp .clinerules (đặc biệt: bảo mật API Key, Triple-Filter Protocol).
3. Không bao giờ đoán mò (Zero-Guessing). Nếu thiếu context, hãy hỏi.
4. Trả lời bằng tiếng Việt nếu Admin viết tiếng Việt.
5. Khi cần thao tác file/terminal, hãy GỌI TOOL (function call), không tự bịa kết quả.
""")

    # 2. Load .clinerules (Hiến pháp)
    clinerules_path = root / ".clinerules"
    if clinerules_path.exists():
        content = clinerules_path.read_text(encoding="utf-8", errors="replace")
        # Giới hạn 3000 ký tự để không nổ context
        if len(content) > 3000:
            content = content[:3000] + "\n... (cắt ngắn)"
        parts.append(f"\n--- HIẾN PHÁP (.clinerules) ---\n{content}")

    # 3. Load GLOBAL_STATE.md
    gs_path = root / "context" / "GLOBAL_STATE.md"
    if gs_path.exists():
        content = gs_path.read_text(encoding="utf-8", errors="replace")
        if len(content) > 2000:
            content = content[:2000] + "\n... (cắt ngắn)"
        parts.append(f"\n--- GLOBAL STATE ---\n{content}")

    # 4. Load ACTIVE_THOUGHTS.md (chỉ phần đầu)
    at_path = root / "context" / "ACTIVE_THOUGHTS.md"
    if at_path.exists():
        content = at_path.read_text(encoding="utf-8", errors="replace")
        # Chỉ lấy 1500 ký tự đầu (current session)
        if len(content) > 1500:
            content = content[:1500] + "\n... (cắt ngắn)"
        parts.append(f"\n--- ACTIVE THOUGHTS (Recent) ---\n{content}")

    return "\n".join(parts)