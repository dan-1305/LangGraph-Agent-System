@echo off
echo ======================================================
echo 🚀 KICH HOAT RAG INGESTION (THU CONG)
echo ======================================================
echo Dang kiem tra tai nguyen he thong...

uv run python tools/system/rag_ingest.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ [LOI] Qua trinh Ingest bi dung do thieu RAM hoac loi he thong.
    echo Vui long tat bot cac ung dung nang va thu lai.
) else (
    echo.
    echo ✅ [THANH CONG] Du lieu da duoc cap nhat vao VectorDB.
)

echo.
pause
