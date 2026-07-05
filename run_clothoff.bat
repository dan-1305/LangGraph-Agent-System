@echo off
color 0A
title Cong Cu ClothOff AI (Mien Phi 100%%)

echo Dang kiem tra moi truong...
if not exist "venv\Scripts\python.exe" (
    echo [LOI] Khong tim thay moi truong venv cua LangGraph.
    echo Vui long chay file nay o thu muc goc LangGraph_Agent_System.
    pause
    exit /b
)

echo Dang bat dau chay Cong cu ClothOff...
echo ----------------------------------------------------
venv\Scripts\python.exe tools\clothoff_hf_cli.py
echo ----------------------------------------------------
pause
