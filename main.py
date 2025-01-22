from data_handler import DataFetcher, DataStorage
from strategy import MovingAverageStrategy
from broker import Broker
from backtester import Backtester


def main():
    """Entry point of the application."""
    # Create instances
    data_fetcher = DataFetcher()
    data_storage = DataStorage()
    strategy = MovingAverageStrategy(short_window=5, long_window=15) # example values
    backtester = Backtester(initial_balance=10000) # Example value
    
    # Fetch data
    try:
        data = data_fetcher.fetch_historical_data(symbol="MSFT", start_date="2023-01-01", end_date="2023-01-31") # Example dates
        data_storage.store_data(symbol="MSFT", data=data)
        data = data_storage.get_data(symbol="MSFT")
    except ValueError as e:
        print(f"Error fetching data: {e}")
        return
    
    # Run backtest
    results = backtester.run_backtest(strategy, data)

    # Print results
    print("Backtest Results:")
    print(f"  Initial Balance: {results['initial_balance']}")
    print(f"  Final Balance: {results['final_balance']}")
    print(f"  Profit: {results['profit']}")
    print(f"  Number of Trades: {results['trades']}")
    print("Transaction History:")
    for transaction in results['transaction_history']:
        print(transaction)

if __name__ == "__main__":
    main()
