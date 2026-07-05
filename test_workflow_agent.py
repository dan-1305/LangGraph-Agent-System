import asyncio
from src.factory.main import main
from src.factory.state import FactoryState
from src.factory.nodes.workflow_agent import workflow_agent_node, AIWorkflowAgent
import json

def test_workflow_node():
    print("Testing Workflow Agent Node...")
    state: FactoryState = {
        "user_requirement": "Hãy chạy kiểm tra code regression guard cho tôi",
        "file_path": "src/base_agent.py",
        "response": ""
    }
    
    agent = AIWorkflowAgent()
    decision = agent.decide_workflow(state)
    print("Decision:")
    print(json.dumps(decision, indent=2, ensure_ascii=False))

    print("\nExecuting Node...")
    new_state = workflow_agent_node(state)
    print("New State Response:")
    print(new_state.get("response"))

if __name__ == "__main__":
    test_workflow_node()
