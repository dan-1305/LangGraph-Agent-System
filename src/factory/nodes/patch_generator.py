import os
import re

def git_patch_node(state: dict):
    """
    Node tạo file .patch dựa trên Draft Code đã được sửa (và pass qua Sandbox).
    Giả lập việc tạo patch dựa trên diff cơ bản (để tiện lợi không cần commit thật).
    """
    print("--- [Git Patch Generator] Kích hoạt ---")
    draft_code = state.get("draft_code_ptr", "")
    
    if not draft_code or "# Fallback" in draft_code:
        print("[Git Patch] Không có code hợp lệ để tạo patch.")
        state["patch_file_ptr"] = ""
        return state
        
    # Trích xuất code trong Markdown
    match = re.search(r"```python(.*?)```", draft_code, re.DOTALL)
    if match:
        clean_code = match.group(1).strip()
    else:
        clean_code = draft_code.strip()
        
    patch_dir = os.path.join("reports", "patches")
    os.makedirs(patch_dir, exist_ok=True)
    patch_path = os.path.join(patch_dir, "remediation_fix.patch")
    
    # Ở mức giả lập, ta ghi luôn nội dung file python thay vì diff phức tạp
    # hoặc tạo file dạng pseudo-patch cho Admin đọc.
    with open(patch_path, "w", encoding="utf-8") as f:
        f.write("--- a/target_file.py\n+++ b/target_file.py\n")
        f.write("@@ BẢN VÁ TỰ ĐỘNG BỞI REMEDIATION AGENT @@\n")
        f.write(clean_code)
        
    print(f"[Git Patch] Đã xuất file patch: {patch_path}")
    state["patch_file_ptr"] = patch_path
    return state
