import asyncio
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from projects.sovereign_terminal.core.mcp_client import mcp_manager

async def test_mcp():
    mcp_config_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Code", "User", "globalStorage", "saoudrizwan.claude-dev", "settings", "cline_mcp_settings.json")
    print(f"Loading config from {mcp_config_path}...")
    mcp_manager.load_config(mcp_config_path)
    
    # Chi test sqlite
    mcp_manager.server_configs = {"sqlite": mcp_manager.server_configs.get("sqlite")}
    
    print("Connecting...")
    await mcp_manager.connect_all()
    
    print("Tools loaded:", mcp_manager.tool_to_server.keys())
    
    if "query" in mcp_manager.tool_to_server:
        print("\nExecuting query on game_vault.db...")
        try:
            res = await mcp_manager.execute_tool("query", {"sql": "SELECT name FROM sqlite_master WHERE type='table';"})
            print("Query Result:\n", res)
        except Exception as e:
            print("Query error:", e)
    else:
        print("'query' tool not found.")

    await mcp_manager.close()

if __name__ == "__main__":
    asyncio.run(test_mcp())
