from strategy import TradingStrategy
import numpy as np

class MACDStrategy(TradingStrategy):
    def __init__(self, short_window: int = 12, long_window: int = 26, signal_window: int = 9) -> None:
        """Constructor."""
        super().__init__(name="MACD Strategy")
        self.short_window = short_window
        self.long_window = long_window
        self.signal_window = signal_window

    def should_buy(self, data_point: dict) -> float:
        """Implements the buy logic based on MACD."""
        if len(self.historical_data) < self.long_window + self.signal_window - 1 :
            return 0

        macd, signal_line, _ = self.calculate_macd(self.historical_data)
        if macd[-1] > signal_line[-1] and macd[-2] <= signal_line[-2]:
            return 1
        return 0

    def should_sell(self, data_point: dict) -> float:
        """Implements the sell logic based on MACD."""
        if len(self.historical_data) < self.long_window + self.signal_window - 1:
            return 0

        macd, signal_line, _ = self.calculate_macd(self.historical_data)
        if macd[-1] < signal_line[-1] and macd[-2] >= signal_line[-2]:
            return 1
        return 0
    
    def calculate_macd(self, data: list) -> tuple[list[float], list[float], list[float]]:
          """Calculates the MACD, Signal Line, and Histogram for the given data list."""
          if len(data) < self.long_window + self.signal_window - 1:
              if len(data) > 0:
                close_price = data[-1]['close']
                return [close_price], [close_price], [0]
              else:
                return [0], [0], [0]

          prices = np.array([d['close'] for d in data])
          ema_short = self._calculate_ema(prices, self.short_window)
          ema_long = self._calculate_ema(prices, self.long_window)
          macd_line = ema_short - ema_long
          signal_line = self._calculate_ema(macd_line, self.signal_window)
          histogram = macd_line[-len(signal_line):] - signal_line
          return macd_line[-len(signal_line):], signal_line, histogram
    
    def _calculate_ema(self, data: np.ndarray, window: int) -> np.ndarray:
        """Calculates the Exponential Moving Average (EMA) for a given data list."""
        alpha = 2 / (window + 1)
        ema = np.zeros_like(data, dtype=float)
        ema[:window] = np.mean(data[:window])
        for i in range(window, len(data)):
          ema[i] = alpha * data[i] + (1 - alpha) * ema[i-1]
        return ema
    

    def update_historical_data(self, data: list):
        """Updates the historical data used by the strategy."""
        self.historical_data = data

    def reset(self):
        """Resets the strategy to its default state."""
        self.historical_data = []
        self.prev_short_ma = 0
        self.prev_long_ma = 0
    
    historical_data = []
    prev_short_ma = 0
    prev_long_ma = 0