from data_handler import DataFetcher, DataStorage
from strategies.moving_average import MovingAverageStrategy
from strategies.RSI import RSIStrategy
from strategies.bollinger_bands import BollingerBandsStrategy
from strategy import TradingStrategy
from broker import Broker
from backtester import Backtester


def main():
    """Entry point of the application."""

    # symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'PFE', 'MRNA', 'BNTX', 'JNJ', 'NVAX'] # Example values
    symbols = ['NFLX', 'DIS', 'T', 'VZ', 'KO', 'PEP', 'MCD', 'SBUX', 'NKE', 'WMT', 'COST', 'PG', 'UNH', 'JPM', 'GS', 'MS', 'BAC', 'C', 'WFC', 'AXP', 'V', 'MA', 'PYPL', 'SQ', 'INTC', 'AMD', 'NVDA', 'QCOM', 'MU', 'TSM', 'IBM', 'ORCL', 'CRM', 'ADBE', 'NOW', 'ZM', 'DOCU', 'WORK', 'SNOW', 'FSLY', 'NET', 'CRWD', 'PANW', 'ZS', 'OKTA', 'SPLK', 'DDOG', 'MDB', 'TWLO', 'AYX', 'COUP', 'BILL', 'U', 'FVRR', 'UPWK', 'ETSY', 'SHOP', 'SE', 'CRSP', 'EDIT', 'NTLA', 'BEAM', 'TWST', 'PACB', 'CDNA', 'VIR', 'MRNA', 'BNTX', 'NVAX', 'INO', 'VXRT', 'MRK', 'ABBV', 'GILD', 'LLY', 'REGN', 'BMY', 'ABBV', 'PFE', 'JNJ', 'AZN', 'SNY', 'NVS', 'GSK', 'MRK', 'BAYRY', 'RHHBY', 'TAK', 'AMGN', 'BIIB', 'VRTX', 'ALXN', 'INCY', 'SGEN', 'CRSP', 'EDIT', 'NTLA', 'BEAM', 'TWST', 'PACB', 'CDNA', 'VIR', 'MRNA', 'BNTX', 'NVAX', 'INO', 'VXRT', 'MRK', 'ABBV', 'GILD', 'LLY', 'REGN', 'BMY', 'ABBV', 'PFE', 'JNJ', 'AZN', 'SNY', 'NVS', 'GSK', 'MRK', 'BAYRY', 'RHHBY', 'TAK', 'AMGN', 'BIIB', 'VRTX', 'ALXN', 'INCY', 'SGEN', 'CRSP', 'EDIT', 'NTLA', 'BEAM', 'TWST', 'PACB', 'CDNA']
    
    max_symbols_length = max([len(symbol) for symbol in symbols])

    print_details = False
    print_history = False

    gains = {}

    movingAverageStrategy = MovingAverageStrategy(short_window=5, long_window=40)
    rsiStrategy = RSIStrategy(period=14, overbought=70, oversold=30)
    bollingerBandsStrategy = BollingerBandsStrategy(period=20, std_dev=2)

    strategies : list[TradingStrategy] = [movingAverageStrategy, rsiStrategy, bollingerBandsStrategy]

    max_name_length = max([len(strategy.name) for strategy in strategies])

    for symbol in symbols:
        print(f"Running backtest for symbol: {symbol}")
        # Create instances
        data_fetcher = DataFetcher()
        data_storage = DataStorage()
        for strategy in strategies:
            strategy.reset()
        backtester = Backtester(initial_balance=10000) # Example value
        
        # Fetch data
        try:
            data = data_fetcher.fetch_historical_data(symbol=symbol, start_date="2022-01-01", end_date="2024-05-30") # Example dates
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
    for strategy, results in gains.items():
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
