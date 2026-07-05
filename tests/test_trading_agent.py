import pytest
from unittest.mock import patch, MagicMock
from projects.ai_trading_agent.src.langgraph_agent import MultiAgentTradingSystem
from projects.ai_trading_agent.src.binance_executor import BinanceExecutor

def test_trading_agent_llm_error_fallback():
    """Test cơ chế bảo vệ khi LLM sập hoặc trả về rỗng (Blank Hallucination)"""
    agent = MultiAgentTradingSystem()
    
    # Mock LLM bị sập hoặc trả về rỗng
    mock_llm = MagicMock()
    mock_llm.invoke.side_effect = Exception("LLM Rate Limit Error")
    
    # Ép system dùng mock LLM
    agent.llm_manager = mock_llm
    
    # Execute fallback
    decision = agent.analyze_and_trade(
        multi_asset_data_str="Fake data", 
        current_portfolio="Fake portfolio", 
        news_list=[]
    )
    
    # Kì vọng fallback về hành động bảo vệ vốn (100% USDT) vì lỗi LLM 
    # Hoặc ít nhất là không crash và có 'reasoning' báo lỗi Fallback
    assert "allocation" in decision
    assert "reasoning" in decision
    assert "Fallback" in decision["reasoning"] or "lỗi" in decision["reasoning"].lower()
    
    # Kiểm tra quy tắc bảo vệ: nếu Fallback thì phải rút về USDT hoặc giữ tỷ trọng cũ
    # _non_ai_fallback sẽ tự động kích hoạt ML, nếu ML rỗng sẽ trả về USDT: 1.0
    if not decision["allocation"]:
        pass # Rỗng cũng ok, BinanceExecutor sẽ bỏ qua
    else:
        assert decision["allocation"].get("USDT", 0) == 1.0

@patch("projects.ai_trading_agent.src.binance_executor.ccxt.binance")
def test_trading_agent_binance_error_fallback(mock_binance_cls):
    """Test cơ chế bảo vệ khi Binance API sập hoặc sai Key (Lỗi -2015)"""
    mock_binance_instance = MagicMock()
    # Giả lập lỗi API -2015 khi gọi hàm fetch_balance
    mock_binance_instance.fetch_balance.side_effect = Exception("Binance API Error -2015: Invalid API-key, IP, or permissions for action.")
    mock_binance_cls.return_value = mock_binance_instance
    
    executor = BinanceExecutor()
    portfolio = executor.get_current_portfolio()
    
    # Không được crash, phải an toàn trả về portfolio mô phỏng hoặc default
    assert isinstance(portfolio, dict)
    assert portfolio.get("USDT") is not None
