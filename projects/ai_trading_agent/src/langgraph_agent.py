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
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
    
from src.base_agent import BaseAgent
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

class GenericAgent(BaseAgent):
    def _ai_handler(self, *args, **kwargs):
        pass
    def _logic_handler(self, *args, **kwargs):
        pass

class MultiAgentTradingSystem(BaseAgent):
    def __init__(self):
        # Kế thừa BaseAgent với label tier-2 (tiết kiệm)
        super().__init__(name="TradingSystem", role="Hệ thống giao dịch đa tác nhân", agent_label="tier-2", temperature=0.1)
        
        # Dùng Risk Manager Label (tier-1) cho các quyết định chốt hạ
        # [FIX] Sử dụng GenericAgent thay vì BaseAgent trực tiếp vì BaseAgent là ABC
        self.risk_manager_agent = GenericAgent(name="RiskManager", role="Giám đốc Quản trị Rủi ro", agent_label="tier-1", temperature=0.1)
        
        # Initialize Funding Rate Monitor (FREE - Coinglass API)
        self.funding_monitor = FundingRateMonitor()
        
        self.graph = self._build_graph()

    def _ai_handler(self, *args, **kwargs):
        """Implement abstract method from BaseAgent"""
        pass

    def _logic_handler(self, *args, **kwargs):
        """Implement abstract method from BaseAgent"""
        return {"final_decision": {"reasoning": "Fallback logic activated.", "allocation": {}, "confidence_score": 0}}

    def _init_node(self, state: TradingState) -> dict:
        """Node khởi tạo để kích hoạt luồng Fan-out"""
        return {
            "tech_analysis": "Đang chờ phân tích...",
            "fundamental_analysis": "Đang chờ phân tích...",
            "sentiment_analysis": "Đang chờ phân tích..."
        }

    def _technical_node(self, state: TradingState) -> dict:
        print("🕵️ [Strategic Advisor] Đang thẩm định Xu hướng Stage 2 (Minervini Standard)...")
        
        tickers_str = Config.TRADE_TICKERS_STR
        
        prompt = f"""Bạn là một Cố vấn Chiến lược (Strategic Advisor) cấp cao, chuyên trách về Swing Trading theo chuẩn Mark Minervini.
Hãy thẩm định dữ liệu {tickers_str}:
{state['market_data']}

Nhiệm vụ: 
1. Thẩm định Trend Template: Xác định tài sản nào hội đủ 6 tiêu chuẩn Stage 2 (Uptrend thực thụ).
2. Đánh giá Margin of Safety: Tính toán khoảng cách tới SMA 200. Nếu quá > 25%, cảnh báo "Overextended".
3. Xác nhận Điểm dừng (Pivot): Tìm kiếm sự siết chặt VCP trước khi bùng nổ.
4. Phân loại tài sản: Leader (Dẫn dắt) hay Laggard (Kẻ chậm chân).

Yêu cầu: Viết báo cáo súc tích, thực tế, không dùng từ ngữ "làm phép"."""
        content = self._call_llm(prompt)
        return {"tech_analysis": content}

    def _sentiment_node(self, state: TradingState) -> dict:
        print("📰 [Sentiment Agent] Đang phân tích tâm lý thị trường theo tư duy 'Trading in the Zone'...")
        prompt = f"""Bạn là một chuyên gia tâm lý giao dịch bậc thầy (Psychology Expert).
Hãy đánh giá dữ liệu và Funding Rate:
{state['news_data']}

Nhiệm vụ:
1. Nhận diện hành vi bầy đàn: Đám đông đang ở trạng thái "Euphoria" (hưng phấn cực độ) hay "Panic" (hoảng loạn)?
2. Phân tích Funding Rate: Nhận diện rủi ro thanh lý (Liquidation risk) khi Funding quá cao hoặc quá thấp.
3. Tin tức Catalyst: Tìm kiếm các sự kiện có khả năng thay đổi cơ bản xu hướng (Earnings, Upgrade, Regs).
4. Whale Alert: Đặc biệt chú ý hành vi của tiền thông minh (Smart Money).

In đậm "[CẢNH BÁO NGUY HIỂM]" nếu phát hiện dấu hiệu lừa đảo (Trap) hoặc biến động cực đoan."""
        content = self._call_llm(prompt)
        return {"sentiment_analysis": content}

    def _fundamental_node(self, state: TradingState) -> dict:
        print("🏢 [Fundamental Analyst] Đang định giá theo 'Biên độ an toàn' và tiềm năng tăng trưởng...")
        prompt = f"""Bạn là một nhà phân tích cơ bản chuyên sâu.
Dữ liệu: {state['fundamental_data']}

Nhiệm vụ:
1. Biên độ an toàn (Margin of Safety): Tính toán khoảng cách từ mức giá hiện tại tới giá trị định giá/đỉnh lịch sử.
2. Chất lượng tăng trưởng: Đánh giá doanh thu, người dùng hoặc dòng tiền (nếu có).
3. Vị thế ngành: Tài sản này là "Category Killer" hay kẻ bám đuôi?
4. Định giá: Nhận diện vùng bong bóng hoặc vùng định giá thấp (Undervalued).

Tuyệt đối KHÔNG đưa ra tỷ lệ phân bổ vốn."""
        content = self._call_llm(prompt)
        return {"fundamental_analysis": content}

    def _risk_manager_node(self, state: TradingState) -> dict:
        print("🛡️ [Sovereign Risk Manager] Đang thực thi Nguyên lý Ray Dalio (Objective Truth)...")
        tickers_list = [t.split('-')[0].strip() for t in Config.TRADE_TICKERS]
        
        # [FIX] Đảm bảo các key tồn tại trong state trước khi truy cập
        tech_report = state.get('tech_analysis', 'Không có dữ liệu kỹ thuật.')
        fund_report = state.get('fundamental_analysis', 'Không có dữ liệu cơ bản.')
        sent_report = state.get('sentiment_analysis', 'Không có dữ liệu tâm lý.')

        prompt = f"""Bạn là Giám đốc Quản lý Rủi ro tối cao (Sovereign Risk Manager). Nhiệm vụ của bạn là đưa ra quyết định phân bổ vốn dựa trên "Sự thật khách quan" (Ray Dalio) và "Bảo vệ vốn tuyệt đối" (Mark Minervini).
Dưới đây là báo cáo từ 3 bộ phận phân tích của bạn:

1. Báo cáo Kỹ thuật & On-chain:
{tech_report}

2. Báo cáo Phân tích Cơ bản & Biên độ an toàn (Value Investing):
{fund_report}

3. Báo cáo Tâm lý (Sentiment) & Bầy đàn:
{sent_report}

Trạng thái Portfolio hiện tại:
{state['current_portfolio']}

Nhiệm vụ của bạn:
Phân bổ lại tỷ trọng danh mục (Portfolio Allocation) dựa trên sự CÂN BẰNG TỔNG HỢP giữa Phân tích Cơ bản (FA), Phân tích Kỹ thuật (TA) và Tâm lý thị trường (Sentiment) của các tài sản: {', '.join(tickers_list)} và tỷ lệ Tiền mặt (USDT).
Tổng tỷ trọng ({' + '.join(tickers_list)} + USDT) PHẢI CHÍNH XÁC BẰNG 1.0 (tương đương 100%).

CÁC NGUYÊN TẮC QUẢN TRỊ RỦI RO CHIẾN THUẬT (MANDATORY RULES):
1. [Nguyên tắc Minervini "Risk-First"]: Luôn ưu tiên đánh giá khả năng sụt giảm trước khi tính lợi nhuận. Tuyệt đối không "Averaging Down" (Bình quân giá xuống). Nếu tài sản đang có xu hướng giảm mạnh (Stage 4) hoặc không có nền tảng tích lũy tốt (Primary Base), hãy hạ tỷ trọng về mức tối thiểu hoặc chuyển sang USDT.
2. [Cắt lỗ và bảo vệ lợi nhuận]: Nếu một tài sản đã đạt mức lợi nhuận đáng kể nhưng TA báo RSI > 75 hoặc MACD giao cắt tử thần, phải thực hiện chốt lời từng phần (Scaling Out) sang USDT để bảo vệ thành quả.
3. [Tâm lý bầy đàn và Định giá cực đoan]: Nếu Sentiment hưng phấn cực độ (Fear & Greed Index > 80) nhưng FA báo giá không còn "Biên độ an toàn" (gần đỉnh 52 tuần), bạn phải quyết liệt chốt lời chuyển sang USDT để phòng ngừa sụp đổ. Ngược lại, khi đám đông bi quan tột độ nhưng FA báo giá có biên độ an toàn cực tốt, hãy "Tham lam" giải ngân mua vào.
4. [L lách rủi ro cực đoan]: Nếu có "[CẢNH BÁO WHALE]" hoặc "[CẢNH BÁO FUNDING RATE]" (Funding Rate cực đoan), bạn bắt buộc phải nâng tỷ trọng USDT tối thiểu lên 30% để phòng thủ, lùi sâu về phòng tuyến chờ thị trường ổn định.

Hãy trả về chuẩn JSON format chính xác như sau (thay các đồng coin tương ứng):
{{
    "reasoning": "Giải thích chi tiết quyết định dựa trên các nguyên lý Minervini, Ray Dalio và bối cảnh FA + TA + Sentiment thực tế.",
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
            # Dùng risk_manager_agent (tier-1) để gọi LLM
            decision = self.risk_manager_agent._call_llm(prompt, is_json=True)
            if not decision:
                raise ValueError("Empty decision from LLM")
        except Exception as e:
            print(f"Lỗi Risk Manager: {e}")
            decision = {
                "reasoning": "Lỗi parse JSON hoặc API. Đề xuất HOLD (Giữ nguyên danh mục).",
                "allocation": {},
                "confidence_score": 0
            }
            
        return {"final_decision": decision}

    def _build_graph(self):
        workflow = StateGraph(TradingState)
        
        # --- Tier 0: Initialization ---
        workflow.add_node("init", self._init_node)

        # --- Tier 1: Parallel Analysis Nodes ---
        workflow.add_node("technical", self._technical_node)
        workflow.add_node("fundamental", self._fundamental_node)
        workflow.add_node("sentiment", self._sentiment_node)
        
        # --- Tier 2: Aggregation & Risk Management ---
        workflow.add_node("risk_manager", self._risk_manager_node)
        
        # --- Graph Routing Logic ---
        workflow.set_entry_point("init")
        
        # Fan-out: Kích hoạt đồng thời 3 node phân tích
        workflow.add_edge("init", "technical")
        workflow.add_edge("init", "fundamental")
        workflow.add_edge("init", "sentiment")
        
        # Fan-in: Hội tụ dữ liệu tại Risk Manager
        workflow.add_edge("technical", "risk_manager")
        workflow.add_edge("fundamental", "risk_manager")
        workflow.add_edge("sentiment", "risk_manager")
        
        workflow.add_edge("risk_manager", END)
        
        return workflow.compile()
        
    def analyze_and_trade(self, multi_asset_data_str, current_portfolio, news_list=None, fundamental_data="", historical_data_df=None):
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
