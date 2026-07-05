import streamlit as st
import functools
import traceback
import logging
from pathlib import Path

def ui_error_guard(func):
    """
    Decorator de bảo vệ UI Streamlit khỏi các lỗi Backend.
    Thay vì hiện Traceback, nó hiện thông báo thân thiện và ghi log ngầm.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # 1. Ghi log lỗi vào file
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            log_file = log_dir / "ui_errors.log"
            
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"\n--- ERROR AT {func.__name__} ---\n")
                f.write(traceback.format_exc())
                f.write("-" * 30 + "\n")
            
            # 2. Hiển thị thông báo thân thiện trên UI
            st.error(f"❌ Co loi xay ra trong qua trinh xu ly!")
            with st.expander("📝 Chi tiet loi (Danh cho ky thuat)"):
                st.code(str(e))
                st.info("💡 Meo: Hay kiem tra lai ket noi mang hoac API Key cua ban.")
            return None
    return wrapper
