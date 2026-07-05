@echo off
chcp 65001 >nul
echo ==================================================
echo 🌟 SOVEREIGN CONTEXT GATHERER FOR GEMINI 🌟
echo ==================================================
echo Đang gọi hệ thống gom dữ liệu từ các file cốt lõi...
echo.

uv run python tools/context_bridge/prepare_gemini_context.py

echo.
echo ==================================================
echo Nhấn phím bất kỳ để thoát...
pause >nul
