import yfinance as yf
from datetime import datetime


class DataFetcher:
    def __init__(self, source_type: str = 'yfinance') -> None:
        """Constructor, sets the data source."""
        self.source_type = source_type

    def fetch_historical_data(self, symbol: str, start_date: str, end_date: str) -> dict:
        """Fetches historical data for a given stock symbol, start date, and end date and returns a dictionary where keys are timestamps (or days) and values are dictionaries with fields like `open`, `high`, `low`, `close`, `volume`.

        Raises:
            ValueError: If the source type is invalid or if there is an error with the data.
        """
        if self.source_type != 'yfinance':
            raise ValueError(f"Invalid source type: {self.source_type}")
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            
            yf_ticker = yf.Ticker(symbol)
            yf_history = yf_ticker.history(start=start, end=end)
            
            data = {}
            for index, row in yf_history.iterrows():
                data[str(index)] = {
                    'open': row['Open'],
                    'high': row['High'],
                    'low': row['Low'],
                    'close': row['Close'],
                    'volume': row['Volume'],
                    'date': str(index)
                }
            return data
        except Exception as e:
            raise ValueError(f"Error fetching data: {e}")


class DataStorage:
    def __init__(self) -> None:
        """Constructor."""
        self.data = {}

    def store_data(self, symbol: str, data: dict) -> None:
        """Stores the fetched data for a given symbol."""
        self.data[symbol] = data

    def get_data(self, symbol: str, time_frame: int = 0) -> list:
        """Returns a list of data points for a given symbol and timeframe (0 for all available data, or number of historical data points to get). Each element in the list is a dictionary like the values from `DataFetcher`.

        Returns:
            list: An empty list if no data is found.
        """
        if symbol not in self.data:
            return []
        
        all_data = list(self.data[symbol].values())
        if time_frame == 0:
            return all_data
        else:
            return all_data[-time_frame:]
