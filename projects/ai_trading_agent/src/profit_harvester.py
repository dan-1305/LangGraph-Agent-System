import pandas as pd
import numpy as np
import logging

class ProfitHarvester:
    """
    He thong thu hoach loi nhuan tu dong (Profit Harvest).
    Trien khai cac chien thuat: Trailing Stop, Partial Take Profit.
    """
    def __init__(self, trailing_percent=0.02, target_profit_levels=[0.05, 0.1, 0.2]):
        self.trailing_percent = trailing_percent
        self.target_profit_levels = target_profit_levels
        self.active_positions = {} # {symbol: {'entry_price': float, 'max_price': float, 'harvested_levels': list}}

    def update_position(self, symbol: str, current_price: float):
        """Cap nhat trang thai vi the va kiem tra diem chot loi."""
        if symbol not in self.active_positions:
            return "HOLD"
            
        pos = self.active_positions[symbol]
        entry_price = pos['entry_price']
        
        # 1. Cap nhat gia cao nhat tung dat duoc (High Water Mark)
        if current_price > pos['max_price']:
            self.active_positions[symbol]['max_price'] = current_price
            
        # 2. Chien thuat Trailing Stop Loss
        max_price = self.active_positions[symbol]['max_price']
        if current_price < max_price * (1 - self.trailing_percent):
            print(f"📉 [TRAILING STOP] Chot loi {symbol} tai {current_price} (Gia dinh: {max_price})")
            return "SELL_ALL"

        # 3. Chien thuat Partial Take Profit
        profit_pct = (current_price - entry_price) / entry_price
        for level in self.target_profit_levels:
            if profit_pct >= level and level not in pos['harvested_levels']:
                self.active_positions[symbol]['harvested_levels'].append(level)
                print(f"💰 [PARTIAL HARVEST] Chot loi 30% {symbol} tai muc +{level*100}%")
                return "SELL_PARTIAL"
        
        return "HOLD"

    def open_position(self, symbol: str, entry_price: float):
        self.active_positions[symbol] = {
            'entry_price': entry_price,
            'max_price': entry_price,
            'harvested_levels': []
        }
        print(f"🚀 Da mo vi the moi cho {symbol} tai gia {entry_price}")

if __name__ == "__main__":
    harvester = ProfitHarvester()
    harvester.open_position("BTC", 60000)
    
    # Gia lap gia tang
    print(f"Update: 62000 -> {harvester.update_position('BTC', 62000)}")
    print(f"Update: 64000 -> {harvester.update_position('BTC', 64000)}") # +6.6% -> Chạm mốc 5%
    
    # Gia lap gia giam dot ngot (Trailing stop)
    print(f"Update: 62500 -> {harvester.update_position('BTC', 62500)}") 
