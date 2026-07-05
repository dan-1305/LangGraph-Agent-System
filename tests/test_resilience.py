import pytest
import sqlite3
import os
from unittest.mock import patch, MagicMock
from src.factory.nodes.router_agent import SemanticRouter, router_node
from src.base_agent import LLMAPIError

DB_PATH = "circuit_breaker.db"

@pytest.fixture
def clean_db():
    """Dọn dẹp DB trước và sau mỗi test"""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    yield
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

def test_router_quota_exhaustion_fallback(clean_db):
    """
    Giả lập lỗi API 429 Too Many Requests để kiểm tra cơ chế Graceful Degradation
    và Audit quá trình ghi log vào SQLite.
    """
    
    # 1. Khởi tạo State đầu vào
    state = {
        "user_requirement": "Phân tích log lỗi 429",
        "file_path": "/var/log/syslog"
    }

    # 2. Mock hàm _call_llm_with_retry của BaseAgent để ném ra LLMAPIError
    with patch('src.base_agent.BaseAgent._call_llm_with_retry') as mock_call:
        # Ép LLM quăng lỗi Rate Limit
        mock_call.side_effect = LLMAPIError("API Rate Limit: 429 Too Many Requests quota exceeded")
        
        # 3. Kích hoạt Router Node (trong node này nó sẽ gọi SemanticRouter.route_query)
        result = router_node(state)
        
        # 4. Kiểm tra Trạng thái Graph
        assert result["selected_workflow"] == "ROUTE_QUOTA_EXHAUSTED", "Graph không chuyển sang trạng thái QUOTA_EXHAUSTED"
        assert "error" in result
        assert "429" in result["error"]
        assert mock_call.call_count == 1, "LLM phải được gọi và bị mock chặn lại"
        
        # 5. Audit Cơ sở dữ liệu SQLite
        assert os.path.exists(DB_PATH), f"File {DB_PATH} không được tạo ra!"
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT failed_node, error_message, state_dump FROM quota_exhaustion_logs")
        rows = cursor.fetchall()
        
        assert len(rows) == 1, "Phải có đúng 1 dòng log được ghi vào DB"
        
        failed_node, error_message, state_dump = rows[0]
        
        assert failed_node == "SemanticRouter"
        assert "429" in error_message
        assert "Phân tích log lỗi 429" in state_dump
        
        conn.close()

if __name__ == "__main__":
    pytest.main(["-v", __file__])
