import yfinance as yf
import pandas as pd
from typing import Dict, List, Optional
import os

class FundamentalAnalyzer:
    """
    Phân tích cơ bản (Fundamental Analysis) dựa trên lý thuyết của Benjamin Graham
    (Nhà Đầu Tư Thông Minh).
    """
    
    def __init__(self):
        pass
        
    def get_fundamental_data(self, symbol: str) -> Dict:
        """
        Lấy các chỉ số tài chính cơ bản của một tài sản.
        Với Crypto (BTC-USD, ETH-USD), yfinance có giới hạn dữ liệu cơ bản,
        nhưng vẫn có thể lấy được Market Cap, Volume, 52-Week High/Low.
        Với Cổ phiếu (ví dụ: AAPL), sẽ lấy được P/E, P/B, EPS.
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Lấy các chỉ số quan trọng
            market_cap = info.get('marketCap', 0)
            current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
            fifty_two_week_high = info.get('fiftyTwoWeekHigh', 0)
            fifty_two_week_low = info.get('fiftyTwoWeekLow', 0)
            
            # Chỉ số cho Cổ phiếu truyền thống
            trailing_pe = info.get('trailingPE', None)
            price_to_book = info.get('priceToBook', None)
            dividend_yield = info.get('dividendYield', 0)
            
            # Tính toán vị trí giá hiện tại so với đỉnh 52 tuần (Đánh giá mức độ FOMO/Sợ hãi)
            drawdown_from_high = 0
            if fifty_two_week_high > 0:
                drawdown_from_high = ((fifty_two_week_high - current_price) / fifty_two_week_high) * 100
                
            return {
                "symbol": symbol,
                "current_price": current_price,
                "market_cap": market_cap,
                "52w_high": fifty_two_week_high,
                "52w_low": fifty_two_week_low,
                "drawdown_from_high_pct": drawdown_from_high,
                "pe_ratio": trailing_pe,
                "pb_ratio": price_to_book,
                "dividend_yield": dividend_yield * 100 if dividend_yield else 0
            }
        except Exception as e:
            print(f"⚠️ Lỗi lấy dữ liệu cơ bản cho {symbol}: {e}")
            return {
                "symbol": symbol,
                "error": str(e)
            }

    def generate_fundamental_report(self, tickers: List[str] = ["BTC-USD", "ETH-USD", "SOL-USD"]) -> str:
        """
        Tạo báo cáo Phân tích Cơ bản dạng chuỗi để nạp cho AI LangGraph.
        """
        report = []
        report.append("==================================================")
        report.append("📊 BÁO CÁO PHÂN TÍCH CƠ BẢN (FUNDAMENTAL & VALUE INVESTING)")
        report.append("==================================================")
        
        for ticker in tickers:
            data = self.get_fundamental_data(ticker)
            if "error" in data:
                report.append(f"❌ {ticker}: Không có dữ liệu.")
                continue
                
            report.append(f"\n📌 TÀI SẢN: {ticker}")
            report.append(f"   Giá hiện tại  : ${data['current_price']:,.2f}")
            report.append(f"   Vốn hóa (Cap) : ${data['market_cap']:,.0f}")
            report.append(f"   Đỉnh 52 tuần  : ${data['52w_high']:,.2f}")
            report.append(f"   Đáy 52 tuần   : ${data['52w_low']:,.2f}")
            
            # Đánh giá Biên độ An toàn (Margin of Safety)
            if data['drawdown_from_high_pct'] > 50:
                safety = "🟢 Tốt (Giảm sâu, có biên độ an toàn cao)"
            elif data['drawdown_from_high_pct'] > 20:
                safety = "🟡 Trung bình (Đang điều chỉnh)"
            else:
                safety = "🔴 Rủi ro cao (Gần đỉnh, dễ đu đỉnh - Cẩn thận bong bóng)"
                
            report.append(f"   Độ sụt giảm   : -{data['drawdown_from_high_pct']:.2f}% từ đỉnh 52 tuần.")
            report.append(f"   Đánh giá Vị thế: {safety}")
            
            if data['pe_ratio']:
                report.append(f"   P/E Ratio     : {data['pe_ratio']:.2f}")
            if data['pb_ratio']:
                report.append(f"   P/B Ratio     : {data['pb_ratio']:.2f}")
                
        report.append("\n💡 LỜI KHUYÊN (BENJAMIN GRAHAM):")
        report.append("- Hãy tham lam khi người khác sợ hãi (Mua khi sụt giảm mạnh).")
        report.append("- Hãy mua tài sản có 'Biên độ an toàn', tránh fomo ở vùng đỉnh 52 tuần.")
        report.append("==================================================")
        
        return "\n".join(report)

if __name__ == "__main__":
    analyzer = FundamentalAnalyzer()
    print(analyzer.generate_fundamental_report())