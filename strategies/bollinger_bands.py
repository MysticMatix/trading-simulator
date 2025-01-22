from strategy import TradingStrategy
import numpy as np

class BollingerBandsStrategy(TradingStrategy):
    def __init__(self, period: int, std_dev: int = 2) -> None:
        """Constructor."""
        super().__init__(name="Bollinger Bands Strategy")
        self.period = period
        self.std_dev = std_dev

    def should_buy(self, data_point: dict) -> float:
      """Implements the buy logic based on Bollinger Bands."""
      if len(self.historical_data) < self.period:
          return 0

      ma, upper_band, lower_band = self.calculate_bollinger_bands(self.historical_data)
      if data_point['close'] < lower_band:
          return 1 # or you can use some scaling to return a value between 0 and 1
      return 0

    def should_sell(self, data_point: dict) -> float:
        """Implements the sell logic based on Bollinger Bands."""
        if len(self.historical_data) < self.period:
            return 0

        ma, upper_band, lower_band = self.calculate_bollinger_bands(self.historical_data)
        if data_point['close'] > upper_band:
            return 1 # or you can use some scaling to return a value between 0 and 1
        return 0

    def calculate_bollinger_bands(self, data: list) -> tuple[float, float, float]:
        """Calculates the Bollinger Bands for a given data list."""
        if len(data) < self.period:
             if len(data) > 0:
                return data[-1]['close'], data[-1]['close'], data[-1]['close']
             else:
                return 0,0,0

        prices = np.array([d['close'] for d in data[-self.period:]])
        ma = np.mean(prices)
        std_dev = np.std(prices)
        upper_band = ma + self.std_dev * std_dev
        lower_band = ma - self.std_dev * std_dev

        return ma, upper_band, lower_band
    
    def update_historical_data(self, data: list):
        """Updates the historical data used by the strategy."""
        self.historical_data = data

    def reset(self):
        """Resets the strategy to its initial state."""
        self.historical_data = []

    historical_data = []