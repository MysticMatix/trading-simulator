from data_handler import DataFetcher, DataStorage
from moving_average_strategy import MovingAverageStrategy
from broker import Broker
from backtester import Backtester


def main():
    """Entry point of the application."""

    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'PFE', 'MRNA', 'BNTX', 'JNJ', 'NVAX'] # Example values
    additional_symbols_long = ['NFLX', 'DIS', 'T', 'VZ', 'KO', 'PEP', 'MCD', 'SBUX', 'NKE', 'WMT', 'COST', 'PG', 'UNH', 'JPM', 'GS', 'MS', 'BAC', 'C', 'WFC', 'AXP', 'V', 'MA', 'PYPL', 'SQ', 'INTC', 'AMD', 'NVDA', 'QCOM', 'MU', 'TSM', 'IBM', 'ORCL', 'CRM', 'ADBE', 'NOW', 'ZM', 'DOCU', 'WORK', 'SNOW', 'FSLY', 'NET', 'CRWD', 'PANW', 'ZS', 'OKTA', 'SPLK', 'DDOG', 'MDB', 'TWLO', 'AYX', 'COUP', 'BILL', 'U', 'FVRR', 'UPWK', 'ETSY', 'SHOP', 'SE', 'CRSP', 'EDIT', 'NTLA', 'BEAM', 'TWST', 'PACB', 'CDNA', 'VIR', 'MRNA', 'BNTX', 'NVAX', 'INO', 'VXRT', 'MRK', 'ABBV', 'GILD', 'LLY', 'REGN', 'BMY', 'ABBV', 'PFE', 'JNJ', 'AZN', 'SNY', 'NVS', 'GSK', 'MRK', 'BAYRY', 'RHHBY', 'TAK', 'AMGN', 'BIIB', 'VRTX', 'ALXN', 'INCY', 'SGEN', 'CRSP', 'EDIT', 'NTLA', 'BEAM', 'TWST', 'PACB', 'CDNA', 'VIR', 'MRNA', 'BNTX', 'NVAX', 'INO', 'VXRT', 'MRK', 'ABBV', 'GILD', 'LLY', 'REGN', 'BMY', 'ABBV', 'PFE', 'JNJ', 'AZN', 'SNY', 'NVS', 'GSK', 'MRK', 'BAYRY', 'RHHBY', 'TAK', 'AMGN', 'BIIB', 'VRTX', 'ALXN', 'INCY', 'SGEN', 'CRSP', 'EDIT', 'NTLA', 'BEAM', 'TWST', 'PACB', 'CDNA']

    print_details = False
    print_history = False

    gains = []

    for symbol in symbols:
        print(f"Running backtest for symbol: {symbol}")
        # Create instances
        data_fetcher = DataFetcher()
        data_storage = DataStorage()
        strategy = MovingAverageStrategy(short_window=5, long_window=40) # example values
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
        results = backtester.run_backtest(strategy, data, multiplier=2)

        gains.append(results['profit_with_stocks'])

        # Print results
        if print_details:
            print("Backtest Results:")
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
    print(f"Total profit with stocks: {sum(gains)}, average profit with stocks: {sum(gains)/len(gains)}")

if __name__ == "__main__":
    main()
