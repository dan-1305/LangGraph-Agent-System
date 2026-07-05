import json
import warnings
from typing import TypedDict
from pathlib import Path

# Import Funding Rate Monitor (FREE - Coinglass API)
from projects.ai_trading_agent.src.funding_rate import FundingRateMonitor

# Whale Alert DISABLED - Costs $30/month, re-enable when profitable
# from whale_alert import WhaleAlertMonitor

# Bỏ qua cảnh báo Pydantic V1 do Langchain chưa nâng cấp đồng bộ
warnings.filterwarnings('ignore', category=UserWarning, module='langchain_core')
warnings.filterwarnings('ignore', category=UserWarning, module='pydantic')
import sys
# Đảm bảo có thể import được thư viện core của dự án
root_dir = Path(__file__).resolve().parent.parent.parent.parent
    
from src.factory.config import create_fallback_chain
from langgraph.graph import StateGraph, END

import projects.ai_trading_agent.src.config as Config_Module
Config = Config_Module.Config

import projects.ai_trading_agent.src.analytics as Analytics_Module
Analytics = Analytics_Module.Analytics

# Định nghĩa State cho LangGraph
class TradingState(TypedDict):
    market_data: str
    news_data: str
    fundamental_data: str
    current_portfolio: str
    tech_analysis: str
    sentiment_analysis: str
    fundamental_analysis: str
    final_decision: dict

class MultiAgentTradingSystem:
    def __init__(self):
        # Dùng model giá rẻ/nhanh cho phân tích đơn lẻ qua Fallback Chain
        self.llm_analyst = create_fallback_chain(
            model_list=["gemini-2.5-flash", "gemini-2.5-flash-lite"], 
            temperature=0.1
        )
        
        # Dùng model xịn cho Risk Manager chốt sổ qua Fallback Chain
        self.llm_manager = create_fallback_chain(
            model_list=["gemini-2.5-pro", "gemini-2.5-flash"], 
            temperature=0.1
        )
        
        # Whale Alert DISABLED - Costs $30/month, re-enable when profitable
        # self.whale_monitor = WhaleAlertMonitor()
        
        # Initialize Funding Rate Monitor (FREE - Coinglass API)
        self.funding_monitor = FundingRateMonitor()
        
        self.graph = self._build_graph()

    def _invoke_with_retry(self, llm, prompt):
        # Tenacity/FallbackChain đã xử lý Retry và Rate Limit ở bên dưới (trong src.base_agent/create_fallback_chain nếu có bọc)
        # Tuy nhiên create_fallback_chain trả về Runnable, gọi invoke() sẽ tự động xoay model.
        try:
            response = llm.invoke(prompt)
            
            # Track token usage
            try:
                from src.token_tracker import track_llm_usage
                model_name = getattr(llm, 'model', 'unknown') if hasattr(llm, 'model') else 'fallback_chain_model'
                track_llm_usage(response, "ai_trading_agent", model_name)
            except Exception as track_e:
                print(f"⚠️ Warning tracking token: {track_e}")
                
            return response
        except Exception as e:
            print(f"❌ [Circuit Breaker Fallback] Thất bại hoàn toàn khi gọi API: {e}")
            class FallbackResponse:
                def __init__(self, content):
                    self.content = content
            # Đảm bảo luồng không bị crash
            return FallbackResponse('{"reasoning": "Circuit Breaker Fallback activated due to API crash. SAFE HOLD.", "allocation": {}, "confidence_score": 0}')

    def _technical_node(self, state: TradingState) -> dict:
        print("🕵️ [Technical Agent] Đang phân tích biểu đồ, chỉ báo và On-chain data...")
        
        tickers_str = Config.TRADE_TICKERS_STR
        
        prompt = f"""Bạn là một chuyên gia phân tích kỹ thuật (Technical Analyst).
Hãy phân tích dữ liệu thị trường của các tài sản {tickers_str} và chỉ số Fear & Greed của những ngày gần nhất:
{state['market_data']}

Nhiệm vụ: Trả về một đoạn văn ngắn gọn đánh giá xu hướng của từng đồng coin (tăng/giảm/đi ngang), tình trạng quá mua/quá bán (dựa vào RSI), và sức mạnh xu hướng (dựa vào SMA 20 và 50). Chú ý đánh giá mức độ rủi ro chung từ Fear & Greed Index và dữ liệu MACD/Bollinger Bands.
Tuyệt đối KHÔNG đưa ra tỷ lệ phân bổ vốn, chỉ phân tích kỹ thuật thuần túy."""
        response = self._invoke_with_retry(self.llm_analyst, prompt)
        return {"tech_analysis": response.content}

    def _sentiment_node(self, state: TradingState) -> dict:
        print("📰 [Sentiment Agent] Đang đọc và đánh giá tin tức thị trường...")
        prompt = f"""Bạn là một chuyên gia phân tích tâm lý thị trường (Sentiment Analyst).
Hãy đọc các tin tức nóng nhất sau đây và các thông số Funding Rate (nếu có):
{state['news_data']}

Nhiệm vụ: Đánh giá tâm lý chung của thị trường là Tích cực (Bullish), Tiêu cực (Bearish) hay Trung lập (Neutral).
Giải thích ngắn gọn tại sao. Đề xuất nhóm tài sản nào đang được hưởng lợi. Đánh giá rủi ro từ Funding Rate (nếu Funding Rate quá dương -> dễ bị thanh lý Long, nếu quá âm -> dễ bị Short Squeeze).
Tuyệt đối KHÔNG đưa ra tỷ lệ phân bổ cụ thể.

ĐẶC BIỆT CHÚ Ý (WHALE ALERT): Nếu bản tin có nhắc đến "Cá voi" (Whale) đang nạp/rút số lượng lớn, hãy in đậm dòng chữ "[CẢNH BÁO WHALE]". Nếu Funding Rate nằm ở mức CỰC ĐOAN (Extreme), hãy in đậm "[CẢNH BÁO FUNDING RATE]"."""
        response = self._invoke_with_retry(self.llm_analyst, prompt)
        return {"sentiment_analysis": response.content}

    def _fundamental_node(self, state: TradingState) -> dict:
        print("🏢 [Fundamental Analyst] Đang định giá tài sản và Biên độ an toàn...")
        prompt = f"""Bạn là một chuyên gia Đầu tư Giá trị (Value Investor) theo trường phái Benjamin Graham.
Hãy phân tích dữ liệu cơ bản sau đây:
{state['fundamental_data']}

Nhiệm vụ: Đánh giá xem tài sản nào đang ở vùng giá quá cao (bong bóng) và tài sản nào đang có 'Biên độ an toàn' tốt dựa vào tỷ lệ sụt giảm từ đỉnh, P/E (nếu có) và vốn hóa.
Tuyệt đối KHÔNG đưa ra tỷ lệ phân bổ vốn cụ thể."""
        response = self._invoke_with_retry(self.llm_analyst, prompt)
        return {"fundamental_analysis": response.content}

    def _risk_manager_node(self, state: TradingState) -> dict:
        print("🛡️ [Risk Manager] Đang phân bổ danh mục đầu tư (Portfolio Allocation)...")
        tickers_list = [t.split('-')[0].strip() for t in Config.TRADE_TICKERS]
        
        prompt = f"""Bạn là Giám đốc Quản lý Rủi ro (Risk Manager) tại quỹ Quant Trading đa tài sản.
Dưới đây là báo cáo từ 3 bộ phận của bạn:

1. Báo cáo Kỹ thuật & On-chain:
{state['tech_analysis']}

2. Báo cáo Phân tích Cơ bản & Biên độ an toàn (Value Investing):
{state['fundamental_analysis']}

3. Báo cáo Tâm lý (Sentiment) & Bầy đàn:
{state['sentiment_analysis']}

Trạng thái Portfolio hiện tại:
{state['current_portfolio']}

Nhiệm vụ của bạn:
Phân bổ lại tỷ trọng danh mục (Portfolio Allocation) dựa trên sự CÂN BẰNG TỔNG HỢP giữa Phân tích Cơ bản (FA), Phân tích Kỹ thuật (TA) và Tâm lý thị trường (Sentiment) của các tài sản: {', '.join(tickers_list)} và tỷ lệ Tiền mặt (USDT).
Tổng tỷ trọng ({' + '.join(tickers_list)} + USDT) PHẢI CHÍNH XÁC BẰNG 1.0 (tương đương 100%).

NGUYÊN TẮC BẮT BUỘC:
- Nếu Báo cáo Tâm lý cho thấy sự hưng phấn cực độ (Bong bóng) nhưng Báo cáo Cơ bản cho thấy giá đã sát "Đỉnh 52 tuần" (không có biên độ an toàn), BẠN PHẢI CHỐT LỜI (Chuyển sang USDT). Đây là nguyên tắc Tâm lý bầy đàn!
- Nếu thị trường xấu (Fear & Greed cực thấp, Sentiment bi quan tột độ), nhưng Báo cáo Cơ bản cho thấy "Biên độ an toàn rất tốt" (Giảm sâu từ đỉnh), HÃY THAM LAM. Hãy phân bổ vốn mua vào!
- Nếu TA đang ở vùng QUÁ MUA (RSI > 75, chạm Band trên), KHÔNG ĐƯỢC MUA ĐUỔI.
- RÀNG BUỘC ĐẶC BIỆT: Nếu có "[CẢNH BÁO WHALE]" hoặc "[CẢNH BÁO FUNDING RATE]", bạn phải đặc biệt cẩn trọng.

Hãy trả về chuẩn JSON format chính xác như sau (thay các đồng coin tương ứng):
{{
    "reasoning": "Giải thích tư duy quản trị rủi ro đa chiều (FA + TA + Sentiment/Bầy đàn).",
    "allocation": {{
        "BTC": 0.4,
        "ETH": 0.2,
        "SOL": 0.1,
        "USDT": 0.3
    }},
    "confidence_score": 1 đến 10
}}
CHỈ TRẢ VỀ ĐÚNG CHUỖI JSON."""
        
        try:
            response = self._invoke_with_retry(self.llm_manager, prompt)
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "{" in content and "}" in content:
                content = content[content.find("{"):content.rfind("}")+1]
            decision = json.loads(content)
        except Exception as e:
            print(f"Lỗi Risk Manager: {e}\nRaw Content: {response.content}")
            decision = {
                "reasoning": "Lỗi parse JSON hoặc API. Đề xuất HOLD (Giữ nguyên danh mục).",
                "allocation": {},
                "confidence_score": 0
            }
            
        return {"final_decision": decision}

    def _build_graph(self):
        workflow = StateGraph(TradingState)
        
        workflow.add_node("technical", self._technical_node)
        workflow.add_node("fundamental", self._fundamental_node)
        workflow.add_node("sentiment", self._sentiment_node)
        workflow.add_node("risk_manager", self._risk_manager_node)
        
        workflow.set_entry_point("technical")
        workflow.add_edge("technical", "fundamental")
        workflow.add_edge("fundamental", "sentiment")
        workflow.add_edge("sentiment", "risk_manager")
        workflow.add_edge("risk_manager", END)
        
        return workflow.compile()
        
    def analyze_and_trade(self, multi_asset_data_str, current_portfolio, news_list=None, fundamental_data=""):
        news_str = "Không có tin tức nào nổi bật."
        if news_list and len(news_list) > 0:
            news_str = "\n".join([f"- {news}" for news in news_list])
        
        funding_summary = ""
        try:
            funding_summary = self.funding_monitor.get_funding_rate_summary(
                symbols=["BTC", "ETH", "SOL"]
            )
            if funding_summary:
                news_str += "\n\n" + funding_summary
        except Exception as e:
            print(f"⚠️ Could not fetch funding rates (system continues): {e}")
            
        if isinstance(current_portfolio, dict):
            current_portfolio = json.dumps(current_portfolio, indent=2)
            
        inputs = {
            "market_data": multi_asset_data_str,
            "news_data": news_str,
            "fundamental_data": fundamental_data,
            "current_portfolio": current_portfolio
        }
        
        result_state = self.graph.invoke(inputs)
        return result_state["final_decision"]