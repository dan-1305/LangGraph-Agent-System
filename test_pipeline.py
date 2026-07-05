import asyncio
import os
import sys

# Khắc phục lỗi in unicode
import codecs
if sys.stdout.encoding != 'utf-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from src.factory.main import main

if __name__ == "__main__":
    print("🚀 Bắt đầu chạy Audit Pipeline trực tiếp để tránh lỗi background timeout...")
    asyncio.run(main(mode="new", project_name="LangGraph_Agent_System", user_requirement="Hãy audit project LangGraph_Agent_System", file_path=""))
