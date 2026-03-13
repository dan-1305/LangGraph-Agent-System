"""
Whale Alert API Integration
Detects large crypto transactions from whales

Documentation: https://whale-alert.io/documentation/api
"""

import requests
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import pandas as pd
from pathlib import Path

class WhaleAlertMonitor:
    """
    Monitor large crypto transactions using Whale Alert API
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Whale Alert Monitor
        
        Args:
            api_key: Whale Alert API key (get from whale-alert.io)
                    If None, will try to get from WHALE_ALERT_API_KEY env var
        """
        self.api_key = api_key or os.getenv("WHALE_ALERT_API_KEY")
        self.base_url = "https://api.whale-alert.io/v1"
        self.timeout = 10  # seconds
        
        if not self.api_key:
            print("⚠️  WARNING: No Whale Alert API key provided")
            print("   Get free API key at: https://whale-alert.io/documentation/api")
            print("   Add to .env: WHALE_ALERT_API_KEY=your_key_here")
    
    def get_transactions(
        self,
        min_value: int = 500000,
        asset: Optional[str] = None,
        hours: int = 24
    ) -> Optional[pd.DataFrame]:
        """
        Get recent large transactions
        
        Args:
            min_value: Minimum transaction value in USD (default: 500k)
            asset: Specific crypto asset (e.g., "bitcoin", "ethereum", "solana")
            hours: Look back period in hours (default: 24h)
            
        Returns:
            DataFrame with transactions or None if error
        """
        if not self.api_key:
            return None
            
        params = {
            "api_key": self.api_key,
            "min_value": min_value,
            "limit": 100
        }
        
        if asset:
            params["asset"] = asset.lower()
        
        try:
            response = requests.get(
                f"{self.base_url}/transactions",
                params=params,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("count", 0) == 0:
                    print(f"🐋 No whale transactions found (min: ${min_value:,})")
                    return None
                
                # Parse transactions
                transactions = []
                for tx in data.get("transactions", []):
                    # Filter by time
                    tx_time = datetime.fromtimestamp(tx["timestamp"])
                    cutoff = datetime.now() - timedelta(hours=hours)
                    
                    if tx_time < cutoff:
                        continue
                        
                    transactions.append({
                        "timestamp": tx_time,
                        "date": tx_time.strftime("%Y-%m-%d"),
                        "time": tx_time.strftime("%H:%M:%S"),
                        "asset": tx.get("symbol", "N/A").upper(),
                        "transaction_type": tx.get("transaction_type", "N/A"),
                        "amount": tx.get("amount", 0),
                        "amount_usd": tx.get("amount_usd", 0),
                        "from_address": tx.get("from", {}).get("address", "N/A")[:10] + "...",
                        "from_type": tx.get("from", {}).get("owner_type", "N/A"),
                        "to_address": tx.get("to", {}).get("address", "N/A")[:10] + "...",
                        "to_type": tx.get("to", {}).get("owner_type", "N/A"),
                        "exchange": tx.get("to", {}).get("owner", "N/A"),
                        "hash": tx.get("hash", "N/A")[:10] + "..."
                    })
                
                df = pd.DataFrame(transactions)
                
                # Format amounts
                df["amount_usd_fmt"] = df["amount_usd"].apply(
                    lambda x: f"${x:,.0f}"
                )
                df["amount_fmt"] = df.apply(
                    lambda row: f"{row['amount']:,.2f} {row['asset']}",
                    axis=1
                )
                
                print(f"🐋 Found {len(df)} whale transactions:")
                for _, row in df.iterrows():
                    print(f"   - {row['amount_fmt']} (${row['amount_usd']:,.0f}) "
                          f"{row['transaction_type']} → {row['to_type']}")
                
                return df
                
            elif response.status_code == 429:
                print("⚠️  Whale Alert API rate limit exceeded")
                return None
            else:
                print(f"❌ Whale Alert API error: {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            print("⚠️  Whale Alert API timeout")
            return None
        except Exception as e:
            print(f"❌ Error fetching whale transactions: {e}")
            return None
    
    def get_exchange_inflow_outflow(
        self,
        asset: str,
        min_value: int = 500000,
        hours: int = 24
    ) -> Dict[str, float]:
        """
        Calculate net flow to/from exchanges
        
        Args:
            asset: Crypto asset (e.g., "bitcoin", "ethereum", "solana")
            min_value: Minimum transaction value in USD
            hours: Look back period in hours
            
        Returns:
            Dict with 'inflow', 'outflow', 'net_flow' values
        """
        df = self.get_transactions(asset=asset, min_value=min_value, hours=hours)
        
        if df is None or df.empty:
            return {"inflow": 0, "outflow": 0, "net_flow": 0}
        
        # Calculate flows
        exchange_in = df[df["to_type"] == "exchange"]["amount_usd"].sum()
        exchange_out = df[df["from_type"] == "exchange"]["amount_usd"].sum()
        net_flow = exchange_in - exchange_out
        
        result = {
            "inflow": exchange_in,
            "outflow": exchange_out,
            "net_flow": net_flow,
            "net_direction": "BULLISH" if net_flow > 0 else "BEARISH",
            "transactions": len(df)
        }
        
        print(f"\n📊 Exchange Flow Analysis ({asset.upper()} - {hours}h):")
        print(f"   Inflow:   ${exchange_in:,.0f}")
        print(f"   Outflow:  ${exchange_out:,.0f}")
        print(f"   Net Flow: ${net_flow:,.0f} ({result['net_direction']})")
        
        return result
    
    def get_whale_alert_summary(
        self,
        assets: List[str] = ["bitcoin", "ethereum", "solana"],
        min_value: int = 500000,
        hours: int = 24
    ) -> str:
        """
        Get formatted summary of whale activity for AI Agent
        
        Args:
            assets: List of assets to monitor
            min_value: Minimum transaction value in USD
            hours: Look back period in hours
            
        Returns:
            Formatted string with whale alerts
        """
        if not self.api_key:
            return "No Whale Alert API key configured"
        
        summary = []
        summary.append("\n" + "=" * 60)
        summary.append("🐋 WHALE ALERT MONITOR")
        summary.append("=" * 60)
        
        significant_alerts = []
        
        for asset in assets:
            flow_data = self.get_exchange_inflow_outflow(
                asset=asset,
                min_value=min_value,
                hours=hours
            )
            
            # Check for significant movements
            abs_net = abs(flow_data["net_flow"])
            if abs_net > 10_000_000:  # $10M threshold
                direction = "🟢 BULLISH" if flow_data["net_flow"] > 0 else "🔴 BEARISH"
                significant_alerts.append(
                    f"\n[🚨 {asset.upper()} WHALE ALERT]\n"
                    f"   Net Flow: ${flow_data['net_flow']:,.0f} ({direction})\n"
                    f"   Transactions: {flow_data['transactions']}"
                )
        
        if significant_alerts:
            summary.extend(significant_alerts)
            summary.append("\n⚠️  RISK MANAGER: Consider adjusting confidence score")
        else:
            summary.append("\n✅ No significant whale movements detected")
        
        summary.append("=" * 60 + "\n")
        
        return "\n".join(summary)


def main():
    """Test Whale Alert Monitor"""
    print("🐋 Testing Whale Alert Monitor...")
    
    monitor = WhaleAlertMonitor()
    
    # Get summary for major assets
    summary = monitor.get_whale_alert_summary(
        assets=["bitcoin", "ethereum", "solana"],
        min_value=500_000,  # $500k minimum
        hours=24
    )
    
    print(summary)
    
    # Get detailed transactions
    print("\n" + "=" * 60)
    print("RECENT BITCOIN WHALE TRANSACTIONS")
    print("=" * 60)
    df = monitor.get_transactions(asset="bitcoin", min_value=1_000_000, hours=48)
    if df is not None:
        print(df[["date", "time", "asset", "amount_usd_fmt", 
                 "transaction_type", "to_type"]].to_string(index=False))


if __name__ == "__main__":
    main()