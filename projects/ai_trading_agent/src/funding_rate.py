"""
Funding Rate Tracker
Monitor funding rates from Coinglass for BTC, ETH, SOL

Documentation: https://www.coinglass.com/api
"""

import requests
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
import os

class FundingRateMonitor:
    """
    Monitor funding rates from major exchanges using Coinglass API
    """
    
    def __init__(self):
        """Initialize Funding Rate Monitor"""
        self.base_url = "https://open-api.coinglass.com/public/v2"
        self.timeout = 10  # seconds
        
    def get_funding_rates(self, symbol: str = "BTC") -> Optional[pd.DataFrame]:
        """
        Get current funding rates for a specific symbol
        
        Args:
            symbol: Crypto symbol (e.g., "BTC", "ETH", "SOL")
            
        Returns:
            DataFrame with funding rates from different exchanges
        """
        try:
            url = f"{self.base_url}/funding_rate/futures"
            params = {"symbol": symbol}
            
            response = requests.get(url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("code") != 0 or not data.get("data"):
                    print(f"⚠️  No funding rate data for {symbol}")
                    return None
                
                # Parse funding rate data
                rates = []
                for item in data["data"]:
                    rates.append({
                        "symbol": symbol,
                        "exchange": item.get("exchangeName", "N/A"),
                        "funding_rate": float(item.get("fundingRate", 0)),
                        "next_funding_time": item.get("nextFundingTime", "N/A"),
                        "open_interest": float(item.get("openInterest", 0)),
                        "mark_price": float(item.get("markPrice", 0)),
                        "index_price": float(item.get("indexPrice", 0))
                    })
                
                df = pd.DataFrame(rates)
                df["funding_rate_pct"] = df["funding_rate"] * 100  # Convert to percentage
                
                # Sort by funding rate
                df = df.sort_values("funding_rate", ascending=False)
                
                return df
                
            else:
                print(f"❌ Coinglass API error: {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            print("⚠️  Coinglass API timeout")
            return None
        except Exception as e:
            print(f"❌ Error fetching funding rates: {e}")
            return None
    
    def get_avg_funding_rate(self, symbol: str = "BTC") -> Dict[str, float]:
        """
        Calculate average funding rate across exchanges
        
        Args:
            symbol: Crypto symbol (e.g., "BTC", "ETH", "SOL")
            
        Returns:
            Dict with average funding rate and sentiment
        """
        df = self.get_funding_rates(symbol)
        
        if df is None or df.empty:
            # Fallback to Binance API
            try:
                binance_url = f"https://fapi.binance.com/fapi/v1/premiumIndex?symbol={symbol.upper()}USDT"
                resp = requests.get(binance_url, timeout=5)
                if resp.status_code == 200:
                    b_data = resp.json()
                    f_rate = float(b_data.get("lastFundingRate", 0))
                    sentiment = "BULLISH (Longs paying Shorts)" if f_rate > 0.0001 else "BEARISH (Shorts paying Longs)" if f_rate < -0.0001 else "NEUTRAL"
                    return {
                        "symbol": symbol,
                        "avg_funding_rate": f_rate,
                        "avg_funding_rate_pct": f_rate * 100,
                        "sentiment": sentiment,
                        "top_exchange": "Binance (Fallback)",
                        "top_rate": f_rate * 100,
                        "exchanges_count": 1
                    }
            except Exception as e:
                print(f"⚠️ Lỗi Binance Fallback: {e}")
                
            return {
                "symbol": symbol,
                "avg_funding_rate": 0,
                "avg_funding_rate_pct": 0,
                "sentiment": "NEUTRAL",
                "top_exchange": "N/A",
                "top_rate": 0,
                "exchanges_count": 0
            }
        
        # Calculate weighted average by open interest
        total_oi = df["open_interest"].sum()
        if total_oi > 0:
            weighted_avg = (df["funding_rate"] * df["open_interest"]).sum() / total_oi
        else:
            weighted_avg = df["funding_rate"].mean()
        
        # Determine sentiment
        if weighted_avg > 0.0001:  # > 0.01% positive
            sentiment = "BULLISH (Longs paying Shorts)"
        elif weighted_avg < -0.0001:  # < -0.01% negative
            sentiment = "BEARISH (Shorts paying Longs)"
        else:
            sentiment = "NEUTRAL"
        
        # Get top exchange by funding rate
        top_exchange = df.iloc[0]
        
        return {
            "symbol": symbol,
            "avg_funding_rate": weighted_avg,
            "avg_funding_rate_pct": weighted_avg * 100,
            "sentiment": sentiment,
            "top_exchange": top_exchange["exchange"],
            "top_rate": top_exchange["funding_rate_pct"],
            "exchanges_count": len(df)
        } if not df.empty else {
            "symbol": symbol,
            "avg_funding_rate": 0,
            "avg_funding_rate_pct": 0,
            "sentiment": "NEUTRAL",
            "top_exchange": "N/A",
            "top_rate": 0,
            "exchanges_count": 0
        }
    
    def get_funding_rate_summary(
        self,
        symbols: List[str] = ["BTC", "ETH", "SOL"]
    ) -> str:
        """
        Get formatted summary of funding rates for AI Agent
        
        Args:
            symbols: List of symbols to monitor
            
        Returns:
            Formatted string with funding rate analysis
        """
        summary = []
        summary.append("\n" + "=" * 60)
        summary.append("📊 FUNDING RATE MONITOR (Coinglass)")
        summary.append("=" * 60)
        
        extreme_positions = []
        
        for symbol in symbols:
            data = self.get_avg_funding_rate(symbol)
            
            summary.append(f"\n📌 {symbol.upper()}:")
            summary.append(f"   Avg Rate: {data['avg_funding_rate_pct']:+.4f}%")
            summary.append(f"   Sentiment: {data['sentiment']}")
            summary.append(f"   Top Exchange: {data['top_exchange']} ({data['top_rate']:+.4f}%)")
            summary.append(f"   Exchanges: {data['exchanges_count']}")
            
            # Check for extreme positions
            abs_rate = abs(data["avg_funding_rate"])
            if abs_rate > 0.0005:  # > 0.05% (very high)
                direction = "🟢 EXTREME BULLISH" if data["avg_funding_rate"] > 0 else "🔴 EXTREME BEARISH"
                extreme_positions.append(
                    f"\n[🚨 {symbol.upper()} EXTREME FUNDING]\n"
                    f"   Rate: {data['avg_funding_rate_pct']:+.4f}% ({direction})\n"
                    f"   RISK: Potential reversal imminent!"
                )
        
        if extreme_positions:
            summary.extend(extreme_positions)
            summary.append("\n⚠️  RISK MANAGER: High funding rates suggest overcrowded positions")
        else:
            summary.append("\n✅ Funding rates are within normal ranges")
        
        summary.append("=" * 60 + "\n")
        
        return "\n".join(summary)
    
    def get_funding_rate_history(
        self,
        symbol: str = "BTC",
        interval: str = "1h",
        limit: int = 24
    ) -> Optional[pd.DataFrame]:
        """
        Get historical funding rates
        
        Args:
            symbol: Crypto symbol
            interval: Time interval (1h, 4h, 1d)
            limit: Number of data points
            
        Returns:
            DataFrame with historical funding rates
        """
        try:
            url = f"{self.base_url}/funding_rate/history"
            params = {
                "symbol": symbol,
                "interval": interval,
                "size": limit
            }
            
            response = requests.get(url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("code") != 0 or not data.get("data"):
                    print(f"⚠️  No historical funding data for {symbol}")
                    return None
                
                # Parse historical data
                history = []
                for item in data["data"]:
                    history.append({
                        "timestamp": datetime.fromtimestamp(item["fundingTime"] / 1000),
                        "funding_rate": float(item["fundingRate"]),
                        "funding_rate_pct": float(item["fundingRate"]) * 100,
                        "symbol": symbol
                    })
                
                df = pd.DataFrame(history)
                df = df.sort_values("timestamp")
                
                return df
                
            else:
                print(f"❌ Coinglass API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error fetching funding rate history: {e}")
            return None


def main():
    """Test Funding Rate Monitor"""
    print("📊 Testing Funding Rate Monitor...")
    
    monitor = FundingRateMonitor()
    
    # Get summary for major assets
    summary = monitor.get_funding_rate_summary(
        symbols=["BTC", "ETH", "SOL"]
    )
    
    print(summary)
    
    # Get detailed BTC funding rates
    print("\n" + "=" * 60)
    print("DETAILED BTC FUNDING RATES BY EXCHANGE")
    print("=" * 60)
    df = monitor.get_funding_rates("BTC")
    if df is not None:
        print(df[["exchange", "funding_rate_pct", "open_interest", 
                 "mark_price"]].to_string(index=False))
    
    # Get historical funding rates
    print("\n" + "=" * 60)
    print("BTC FUNDING RATE HISTORY (Last 24 hours)")
    print("=" * 60)
    history = monitor.get_funding_rate_history("BTC", interval="1h", limit=24)
    if history is not None:
        print(history[["timestamp", "funding_rate_pct"]].to_string(index=False))


if __name__ == "__main__":
    main()