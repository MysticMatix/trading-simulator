from data_handler import DataFetcher, DataStorage

from strategies.basic.moving_average import MovingAverageStrategy
from strategies.basic.RSI import RSIStrategy
from strategies.basic.bollinger_bands import BollingerBandsStrategy
from strategies.basic.stochastic_oscillator import StochasticOscillatorStrategy
from strategies.basic.macd import MACDStrategy
from strategies.basic.ichimoku_cloud import IchimokuCloudStrategy
from strategies.basic.adx import ADXStrategy

from strategies.hybrid.basic import HybridStrategy
from strategies.hybrid.custom import CustomStrategy

from strategy import TradingStrategy
from broker import Broker
from backtester import Backtester
from tqdm import tqdm


def main():
    """Entry point of the application."""

    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'PFE', 'MRNA', 'BNTX', 'JNJ', 'NVAX'] # Example values
    # symbols = [
    #     "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "INTC", "AMD", "IBM", "ORCL",
    #     "ZM", "PYPL", "NFLX", "META", "ADBE", "CSCO", "CRM", "SHOP", "SQ", "TWLO",
    #     "UBER", "LYFT", "ABNB", "SNAP", "BABA", "TSM", "V", "MA", "JPM", "BAC",
    #     "WFC", "GS", "MS", "C", "T", "VZ", "KO", "PEP", "NKE", "HD",
    #     "WMT", "COST", "MCD", "SBUX", "DIS", "BA", "CAT", "XOM", "CVX", "BP",
    #     "PFE", "MRNA", "JNJ", "BNTX", "MRK", "ABBV", "GILD", "CVS", "UNH", "TMO",
    #     "UPS", "FDX", "DE", "GM", "F", "RIVN", "LCID", "RCL", "CCL", "DAL",
    #     "AAL", "UAL", "LUV", "GE", "HON", "MMM", "DOW", "GLW", "APD", "BK",
    #     "TROW", "VFC", "AMAT", "QCOM", "MU", "TXN", "FSLR", "RUN", "PLUG",
    #     "COP", "SLB", "HAL", "MRO", "EOG", "LMT", "RTX", "GD", "NOC", "PYPL",
    #     "ADSK", "EA", "TTWO", "MTCH", "BKNG", "DPZ", "MAR", "HAS", "MAT"
    # ]

    symbols = sorted(symbols)
    
    max_symbols_length = max([len(symbol) for symbol in symbols]) + 2

    print_details = False
    print_history = False

    gains = {}

    movingAverageStrategy = MovingAverageStrategy(short_window=5, long_window=40)
    rsiStrategy = RSIStrategy(period=14, overbought=70, oversold=30)
    bollingerBandsStrategy = BollingerBandsStrategy(period=20, std_dev=2)
    stochasticOscillatorStrategy = StochasticOscillatorStrategy(period=20, overbought=80, oversold=20)
    macdStrategy = MACDStrategy(short_window=12, long_window=26, signal_window=9)
    ichimokuCloudStrategy = IchimokuCloudStrategy()
    adxStrategy = ADXStrategy(period=20)

    ichimokuADX = HybridStrategy([IchimokuCloudStrategy(), ADXStrategy(period=20)], weights=[0.5, 0.5], name="Ichimoku + ADX")
    ichimokuADX2 = CustomStrategy([IchimokuCloudStrategy(), ADXStrategy(period=20)], buy_merging_function=lambda x: x[0] * x[1], sell_merging_function=lambda x: x[0] * x[1], name="Ichimoku * ADX")

    strategies : list[TradingStrategy] = [
        movingAverageStrategy,
        rsiStrategy,
        bollingerBandsStrategy,
        stochasticOscillatorStrategy,
        macdStrategy,
        adxStrategy,
        ichimokuCloudStrategy,
        ichimokuADX,
        ichimokuADX2
    ]

    max_name_length = max([len(strategy.name) for strategy in strategies])

    for symbol in tqdm(symbols):
        # Create instances
        data_fetcher = DataFetcher()
        data_storage = DataStorage()
        for strategy in strategies:
            strategy.reset()
        backtester = Backtester(initial_balance=10000) # Example value
        
        # Fetch data
        try:
            data = data_fetcher.fetch_historical_data(symbol=symbol, start_date="2024-01-01", end_date="2024-05-30") # Example dates
            data_storage.store_data(symbol=symbol, data=data)
            data = data_storage.get_data(symbol=symbol)
        except ValueError as e:
            print(f"Error fetching data: {e}")
            return
        
        if len(data) == 0:
            print(f"No data found for symbol: {symbol}")
            continue
        
        # Run backtest
        for strategy in strategies:
            results = backtester.run_backtest(strategy, data, multiplier=2, symbol=symbol)

            if not strategy.name in gains:
                gains[strategy.name] = {}
            gains[strategy.name][symbol] = results['profit_with_stocks']

            # Print results
            if print_details:
                print("Backtest Results for", strategy.name)
                print(f"  Initial Balance: {results['initial_balance']}")
                print(f"  Final Balance: {results['final_balance']}")
                print(f"  Final Balance with Stocks: {results['final_balance_with_stocks']}")
                print(f"  Profit: {results['profit']}")
                print(f"  Profit with Stocks: {results['profit_with_stocks']}")
                print(f"  Number of Trades: {results['trades']}")
                if print_history:
                    print("Transaction History:")
                    for transaction in results['transaction_history']:
                        print(transaction)

    

    print()
    for strategy, results in sorted(gains.items(), key=lambda x: sum(x[1].values()), reverse=True):
        if print_details:
            print()
            print(f"Results for {strategy}")
            for symbol, gain in results.items():
                print(f"  {symbol}: {gain}")
        average_gain = sum(results.values()) / len(results)
        min_gain = min(results.values())
        min_gain_symbol = f"({[symbol for symbol, gain in results.items() if gain == min_gain][0]})"
        max_gain = max(results.values())
        max_gain_symbol = f"({[symbol for symbol, gain in results.items() if gain == max_gain][0]})"
        median_gain = sorted(results.values())[len(results) // 2]

        print(f"{strategy.ljust(max_name_length)} | Avg: {average_gain:8.4f}  Min: {min_gain:8.2f} {min_gain_symbol.ljust(max_symbols_length)}  Max: {max_gain:8.2f} {max_gain_symbol.ljust(max_symbols_length)}  Median: {median_gain:8.2f}")

if __name__ == "__main__":
    main()
