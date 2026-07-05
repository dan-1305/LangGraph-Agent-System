import os
import sys
import json
import asyncio
import io
from pathlib import Path

# Force UTF-8 for prints
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
from typing import Dict, Any, List, Optional
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession

class MCPManager:
    def __init__(self):
        self.server_configs: Dict[str, dict] = {}
        self.sessions: Dict[str, ClientSession] = {}
        self._exit_stack = None
        self.available_tools: List[dict] = []
        self.tool_to_server: Dict[str, str] = {}

    def load_config(self, config_path: str):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.server_configs = data.get("mcpServers", {})
        except Exception as e:
            print(f"[MCP] Không thể đọc config {config_path}: {e}")

    async def connect_all(self):
        from contextlib import AsyncExitStack
        self._exit_stack = AsyncExitStack()
        
        for server_name, config in self.server_configs.items():
            if config.get("disabled", False):
                continue
            
            command = config.get("command")
            args = config.get("args", [])
            env = config.get("env", None)
            if not env:
                env = os.environ.copy()
            else:
                merged_env = os.environ.copy()
                merged_env.update(env)
                env = merged_env

            server_params = StdioServerParameters(
                command=command,
                args=args,
                env=env
            )
            
            try:
                # Enter stdio_client context
                transport = await self._exit_stack.enter_async_context(stdio_client(server_params))
                read, write = transport
                
                # Enter session context
                session = await self._exit_stack.enter_async_context(ClientSession(read, write))
                await session.initialize()
                
                self.sessions[server_name] = session
                print(f"[MCP] Đã kết nối server: {server_name}")
                
                # Fetch tools
                tools_response = await session.list_tools()
                for tool in tools_response.tools:
                    tool_def = {
                        "type": "function",
                        "function": {
                            "name": tool.name,
                            "description": tool.description or f"MCP Tool: {tool.name}",
                            "parameters": tool.inputSchema
                        }
                    }
                    self.available_tools.append(tool_def)
                    self.tool_to_server[tool.name] = server_name
                    
            except Exception as e:
                print(f"[MCP] Lỗi kết nối {server_name}: {e}")

    async def execute_tool(self, tool_name: str, arguments: dict) -> str:
        server_name = self.tool_to_server.get(tool_name)
        if not server_name:
            return f"[ERROR] Không tìm thấy MCP server cho tool: {tool_name}"
            
        session = self.sessions.get(server_name)
        if not session:
            return f"[ERROR] Session cho {server_name} không hoạt động."
            
        try:
            result = await session.call_tool(tool_name, arguments)
            if result.isError:
                return f"[MCP ERROR] {result.content}"
            # Extract text from result content
            output = []
            for item in result.content:
                if item.type == "text":
                    output.append(item.text)
                else:
                    output.append(str(item))
            return "\n".join(output)
        except Exception as e:
            return f"[ERROR] Lỗi thực thi {tool_name}: {e}"

    async def close(self):
        if self._exit_stack:
            await self._exit_stack.aclose()
            print("[MCP] Đã đóng tất cả kết nối.")

mcp_manager = MCPManager()
