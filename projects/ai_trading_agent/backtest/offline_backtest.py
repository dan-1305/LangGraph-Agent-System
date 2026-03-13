"""
Offline Backtest Mode
Test trading strategies using historical data without live API calls

This mode allows backtesting strategies offline:
- Uses historical data from SQLite database
- Simulates trading without real money
- No API calls needed (except for AI models)
- Perfect for strategy development and testing
"""

import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

class OfflineBacktester:
    """
    Offline backtest engine for AI Trading strategies
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize backtester
        
        Args:
            db_path: Path to trading_market.db (auto-detected if None)
        """
        if db_path is None:
            base_dir = Path(__file__).resolve().parent.parent.parent
            db_path = base_dir / "data" / "trading_market.db"
        
        self.db_path = db_path
        self.conn = None
        
        # Default backtest parameters
        self.initial_capital = 100_000  # $100,000
        self.commission = 0.001  # 0.1% per trade
        self.slippage = 0.0005  # 0.05% slippage
        
    def connect(self):
        """Connect to database"""
        self.conn = sqlite3.connect(self.db_path)
        return self
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def __enter__(self):
        return self.connect()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def get_historical_data(
        self,
        ticker: str = "BTC_USD",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        days: int = 90
    ) -> pd.DataFrame:
        """
        Get historical OHLCV data with indicators
        
        Args:
            ticker: Ticker symbol (e.g., "BTC_USD")
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            days: Number of days to fetch if dates not specified
            
        Returns:
            DataFrame with OHLCV + indicators
        """
        if not self.conn:
            raise RuntimeError("Database connection not established. Use with context manager.")
        
        # Determine date range
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        query = f"""
        SELECT * FROM {ticker}
        WHERE Date >= '{start_date}' AND Date <= '{end_date}'
        ORDER BY Date
        """
        
        df = pd.read_sql(query, self.conn)
        df['Date'] = pd.to_datetime(df['Date'])
        
        return df
    
    def generate_signals(
        self,
        df: pd.DataFrame,
        strategy: str = "combined"
    ) -> pd.DataFrame:
        """
        Generate trading signals based on indicators
        
        Args:
            df: DataFrame with OHLCV + indicators
            strategy: Strategy type ('rsi', 'macd', 'bb', 'combined')
            
        Returns:
            DataFrame with 'signal' column (1=buy, -1=sell, 0=hold)
        """
        df = df.copy()
        df['signal'] = 0
        
        if strategy == "rsi":
            # RSI Strategy
            df.loc[df['RSI_14'] < 30, 'signal'] = 1  # Oversold -> Buy
            df.loc[df['RSI_14'] > 70, 'signal'] = -1  # Overbought -> Sell
        
        elif strategy == "macd":
            # MACD Crossover Strategy
            df['macd_cross'] = df['MACD'] > df['MACD_Signal']
            df['macd_cross_prev'] = df['macd_cross'].shift(1)
            df.loc[(df['macd_cross'] == True) & (df['macd_cross_prev'] == False), 'signal'] = 1
            df.loc[(df['macd_cross'] == False) & (df['macd_cross_prev'] == True), 'signal'] = -1
        
        elif strategy == "bb":
            # Bollinger Bands Strategy
            df['bb_position'] = (df['Close'] - df['BB_Lower']) / (df['BB_Upper'] - df['BB_Lower'])
            df.loc[df['bb_position'] < 0.1, 'signal'] = 1  # Near lower band -> Buy
            df.loc[df['bb_position'] > 0.9, 'signal'] = -1  # Near upper band -> Sell
        
        elif strategy == "combined":
            # Combined Strategy (all signals)
            df.loc[df['RSI_14'] < 30, 'signal'] += 1
            df.loc[df['RSI_14'] > 70, 'signal'] -= 1
            
            df['macd_cross'] = df['MACD'] > df['MACD_Signal']
            df['macd_cross_prev'] = df['macd_cross'].shift(1)
            df.loc[(df['macd_cross'] == True) & (df['macd_cross_prev'] == False), 'signal'] += 1
            df.loc[(df['macd_cross'] == False) & (df['macd_cross_prev'] == True), 'signal'] -= 1
            
            df['bb_position'] = (df['Close'] - df['BB_Lower']) / (df['BB_Upper'] - df['BB_Lower'])
            df.loc[df['bb_position'] < 0.1, 'signal'] += 1
            df.loc[df['bb_position'] > 0.9, 'signal'] -= 1
            
            # Normalize to -1, 0, 1
            df.loc[df['signal'] > 0, 'signal'] = 1
            df.loc[df['signal'] < 0, 'signal'] = -1
        
        return df
    
    def backtest(
        self,
        ticker: str = "BTC_USD",
        strategy: str = "combined",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        days: int = 90,
        initial_capital: float = 100_000
    ) -> Dict:
        """
        Run backtest simulation
        
        Args:
            ticker: Ticker symbol
            strategy: Strategy type
            start_date: Start date
            end_date: End date
            days: Number of days
            initial_capital: Starting capital
            
        Returns:
            Dict with backtest results
        """
        # Get historical data
        df = self.get_historical_data(ticker, start_date, end_date, days)
        
        if df.empty:
            return {"error": f"No data found for {ticker}"}
        
        # Generate signals
        df = self.generate_signals(df, strategy)
        
        # Simulation variables
        capital = initial_capital
        position = 0  # Position size (negative = short)
        entry_price = 0
        trades = []
        
        # Simulate trades
        for idx, row in df.iterrows():
            price = row['Close']
            signal = row['signal']
            
            # Execute trades
            if signal == 1 and position == 0:
                # Buy
                shares = capital / price * (1 - self.commission)
                position = shares
                entry_price = price
                trades.append({
                    'date': row['Date'],
                    'action': 'BUY',
                    'price': price,
                    'shares': shares,
                    'capital': capital
                })
                capital = 0
                
            elif signal == -1 and position > 0:
                # Sell
                capital = position * price * (1 - self.commission - self.slippage)
                trades.append({
                    'date': row['Date'],
                    'action': 'SELL',
                    'price': price,
                    'shares': position,
                    'capital': capital,
                    'pnl': (price - entry_price) / entry_price * 100
                })
                position = 0
                entry_price = 0
        
        # Close final position
        if position > 0:
            final_price = df.iloc[-1]['Close']
            capital = position * final_price * (1 - self.commission - self.slippage)
            trades.append({
                'date': df.iloc[-1]['Date'],
                'action': 'SELL',
                'price': final_price,
                'shares': position,
                'capital': capital,
                'pnl': (final_price - entry_price) / entry_price * 100
            })
        
        # Calculate metrics
        final_capital = capital
        total_return = (final_capital - initial_capital) / initial_capital * 100
        
        # Buy & Hold benchmark
        first_price = df.iloc[0]['Close']
        last_price = df.iloc[-1]['Close']
        buy_hold_return = (last_price - first_price) / first_price * 100
        
        # Win rate
        winning_trades = [t for t in trades if 'pnl' in t and t['pnl'] > 0]
        losing_trades = [t for t in trades if 'pnl' in t and t['pnl'] <= 0]
        win_rate = len(winning_trades) / len([t for t in trades if 'pnl' in t]) * 100 if trades else 0
        
        # Max drawdown
        df['cumulative'] = float(initial_capital)
        current_capital = float(initial_capital)
        for idx, row in df.iterrows():
            current_capital = current_capital * (row['Close'] / row['Open'])
            df.loc[idx, 'cumulative'] = current_capital
        
        df['running_max'] = df['cumulative'].cummax()
        df['drawdown'] = (df['cumulative'] - df['running_max']) / df['running_max'] * 100
        max_drawdown = df['drawdown'].min()
        
        results = {
            'ticker': ticker,
            'strategy': strategy,
            'start_date': df.iloc[0]['Date'].strftime('%Y-%m-%d'),
            'end_date': df.iloc[-1]['Date'].strftime('%Y-%m-%d'),
            'initial_capital': initial_capital,
            'final_capital': final_capital,
            'total_return': total_return,
            'buy_hold_return': buy_hold_return,
            'alpha': total_return - buy_hold_return,
            'total_trades': len([t for t in trades if 'pnl' in t]),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': win_rate,
            'max_drawdown': max_drawdown,
            'trades': trades
        }
        
        return results
    
    def compare_strategies(
        self,
        ticker: str = "BTC_USD",
        days: int = 90
    ) -> pd.DataFrame:
        """
        Compare multiple strategies
        
        Args:
            ticker: Ticker symbol
            days: Number of days
            
        Returns:
            DataFrame with comparison results
        """
        strategies = ['rsi', 'macd', 'bb', 'combined']
        results = []
        
        for strategy in strategies:
            result = self.backtest(ticker, strategy, days=days)
            if 'error' not in result:
                results.append({
                    'Strategy': strategy.upper(),
                    'Total Return': f"{result['total_return']:.2f}%",
                    'Buy & Hold': f"{result['buy_hold_return']:.2f}%",
                    'Alpha': f"{result['alpha']:.2f}%",
                    'Win Rate': f"{result['win_rate']:.1f}%",
                    'Max Drawdown': f"{result['max_drawdown']:.2f}%",
                    'Trades': result['total_trades']
                })
        
        return pd.DataFrame(results)
    
    def print_results(self, results: Dict):
        """Print backtest results in a formatted way"""
        print("\n" + "=" * 60)
        print(f"📊 BACKTEST RESULTS - {results['ticker']}")
        print("=" * 60)
        print(f"\nStrategy: {results['strategy'].upper()}")
        print(f"Period: {results['start_date']} to {results['end_date']}")
        print(f"\n💰 Capital:")
        print(f"   Initial: ${results['initial_capital']:,.2f}")
        print(f"   Final:   ${results['final_capital']:,.2f}")
        print(f"\n📈 Performance:")
        print(f"   Total Return:  {results['total_return']:+.2f}%")
        print(f"   Buy & Hold:   {results['buy_hold_return']:+.2f}%")
        print(f"   Alpha:         {results['alpha']:+.2f}%")
        print(f"\n📊 Trading:")
        print(f"   Total Trades:  {results['total_trades']}")
        print(f"   Winning:      {results['winning_trades']}")
        print(f"   Losing:       {results['losing_trades']}")
        print(f"   Win Rate:     {results['win_rate']:.1f}%")
        print(f"   Max Drawdown: {results['max_drawdown']:.2f}%")
        print("=" * 60 + "\n")


def main():
    """Run offline backtest demo"""
    print("🚀 OFFLINE BACKTEST MODE")
    print("=" * 60)
    
    # Initialize backtester
    with OfflineBacktester() as backtester:
        
        # Test single strategy
        print("\n📌 Testing COMBINED strategy on BTC_USD...")
        results = backtester.backtest(
            ticker="BTC_USD",
            strategy="combined",
            days=90
        )
        backtester.print_results(results)
        
        # Compare strategies
        print("\n📌 Comparing all strategies...")
        comparison = backtester.compare_strategies("BTC_USD", days=90)
        print(comparison.to_string(index=False))
        
        # Test ETH
        print("\n📌 Testing COMBINED strategy on ETH_USD...")
        eth_results = backtester.backtest(
            ticker="ETH_USD",
            strategy="combined",
            days=90
        )
        backtester.print_results(eth_results)


if __name__ == "__main__":
    main()