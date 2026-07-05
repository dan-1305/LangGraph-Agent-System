@echo off
set PYTHONPATH=.
set PYTHONIOENCODING=utf8
echo [STEP 1] Running Full Text Parser...
uv run python projects\universal_game_vault\src\processors\full_text_parser.py
echo [STEP 2] Running Advanced Extractor...
uv run python projects\universal_game_vault\src\processors\advanced_extractor.py
echo [STEP 3] Running Database Sync...
uv run python projects\universal_game_vault\src\storage\db_manager.py
echo [DONE] He thong da san sang!
pause
