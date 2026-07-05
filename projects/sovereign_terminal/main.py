#!/usr/bin/env python3
"""
Sovereign Terminal - Headless AI Agent.
Chạy độc lập, không cần Cline/VSCode.

Usage:
    python -m projects.sovereign_terminal.main
    uv run python projects/sovereign_terminal/main.py

Author: CEO Sovereign
"""
import os
import sys
import json
from pathlib import Path

# Add root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# UTF-8 fix for Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import asyncio
from openai import AsyncOpenAI
from projects.sovereign_terminal.core.config import Config
from projects.sovereign_terminal.core.persona import load_persona
from projects.sovereign_terminal.core.tools import TOOL_DEFINITIONS, execute_tool
from projects.sovereign_terminal.core.mcp_client import mcp_manager


def print_banner():
    """In banner khi khởi động."""
    print("=" * 60)
    print("👑 SOVEREIGN TERMINAL v1.0 (HEADLESS AGENT)")
    print("=" * 60)
    print(f"  Model: {Config.DEFAULT_MODEL}")
    print(f"  Endpoint: {Config.BASE_URL}")
    print(f"  Root: {Config.ROOT_DIR}")
    print(f"  Tools: read_file, write_file, run_command, list_files")
    print("=" * 60)
    print("Gõ 'exit' hoặc 'quit' để thoát. Gõ 'reset' để xoá history.")
    print()


async def handle_tool_calls(client, model, messages, tool_calls):
    """
    Xử lý tool calls từ AI, trả về kết quả cho AI.
    Hỗ trợ nhiều tool calls liên tiếp.
    """
    for tool_call in tool_calls:
        func_name = tool_call.function.name
        try:
            func_args = json.loads(tool_call.function.arguments)
        except json.JSONDecodeError:
            func_args = {}
        
        print(f"  🔧 [TOOL] {func_name}({func_args})")
        
        if func_name in mcp_manager.tool_to_server:
            # Gọi MCP tool
            result = await mcp_manager.execute_tool(func_name, func_args)
        else:
            # Gọi local tool
            result = execute_tool(func_name, func_args)
            
        print(f"  📤 [RESULT] {result[:200]}...")
        
        # Thêm kết quả tool vào messages
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result,
        })
    
    # Gọi lại API để AI xử lý kết quả tool
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=Config.TEMPERATURE,
        max_tokens=Config.MAX_TOKENS,
    )
    
    return response.choices[0].message


async def chat_loop(client: AsyncOpenAI, model: str, system_prompt: str):
    """
    Vòng lặp Chat REPL (Read-Eval-Print Loop).
    """
    messages = [{"role": "system", "content": system_prompt}]
    
    while True:
        try:
            user_input = input("\n👑 Admin > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Tạm biệt!")
            break
        
        if not user_input:
            continue
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Tạm biệt!")
            break
        if user_input.lower() == "reset":
            messages = [{"role": "system", "content": system_prompt}]
            print("🔄 Đã xoá history. Bắt đầu session mới.")
            continue
        
        # Thêm user message
        messages.append({"role": "user", "content": user_input})
        
        # Giới hạn history (giữ system + 20 tin gần nhất)
        if len(messages) > Config.MAX_HISTORY + 1:
            messages = [messages[0]] + messages[-Config.MAX_HISTORY:]
        
        # Tổng hợp tất cả definitions (local + MCP)
        all_tools = list(TOOL_DEFINITIONS)
        all_tools.extend(mcp_manager.available_tools)
        
        # Gọi API
        try:
            print("🤖 Đang suy nghĩ...", end="\r")
            
            api_kwargs = {
                "model": model,
                "messages": messages,
                "temperature": Config.TEMPERATURE,
                "max_tokens": Config.MAX_TOKENS,
            }
            if all_tools:
                api_kwargs["tools"] = all_tools
                api_kwargs["tool_choice"] = "auto"
                
            response = await client.chat.completions.create(**api_kwargs)
            
            msg = response.choices[0].message
            
            # Xử lý tool calls nếu có
            max_tool_rounds = 10  # Chống infinite loop
            while msg.tool_calls and max_tool_rounds > 0:
                max_tool_rounds -= 1
                messages.append(msg.model_dump(exclude_none=True))
                msg = await handle_tool_calls(client, model, messages, msg.tool_calls)
            
            # In phản hồi cuối
            if msg.content:
                print(f"\n🤖 {msg.content}")
            
            # Lưu lại vào history
            messages.append({"role": "assistant", "content": msg.content or ""})
            
        except Exception as e:
            print(f"\n❌ Lỗi: {e}")
            # Xóa tin nhắn lỗi khỏi history
            if messages and messages[-1]["role"] == "user":
                messages.pop()


async def async_main():
    """Entry point."""
    # Validate config
    if not Config.validate():
        sys.exit(1)
    
    print_banner()
    
    # Init MCP
    mcp_config_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Code", "User", "globalStorage", "saoudrizwan.claude-dev", "settings", "cline_mcp_settings.json")
    if Path(mcp_config_path).exists():
        print("🔌 Đang khởi tạo MCP Clients...")
        mcp_manager.load_config(mcp_config_path)
        await mcp_manager.connect_all()
        print(f"   Đã nạp {len(mcp_manager.available_tools)} MCP tools.")
    
    # Load persona
    print("🧠 Đang nạp trí nhớ (Persona)...")
    system_prompt = load_persona()
    print(f"   System Prompt: {len(system_prompt)} ký tự")
    
    # Init OpenAI client (GGCHAN endpoint)
    client = AsyncOpenAI(**Config.get_client_config())
    
    # Start chat
    print("\n✅ Sẵn sàng! Hãy ra lệnh cho tôi.\n")
    try:
        await chat_loop(client, Config.DEFAULT_MODEL, system_prompt)
    finally:
        await mcp_manager.close()

def main():
    asyncio.run(async_main())

if __name__ == "__main__":
    main()
