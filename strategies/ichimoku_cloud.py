from strategy import TradingStrategy
import numpy as np

class IchimokuCloudStrategy(TradingStrategy):
    def __init__(self) -> None:
        """Constructor."""
        super().__init__(name="Ichimoku Cloud Strategy")

    def should_buy(self, data_point: dict) -> float:
        """Implements the buy logic based on Ichimoku Cloud."""
        if len(self.historical_data) < 52:
            return 0
        
        tenkan_sen, kijun_sen, senkou_a, senkou_b, chikou_span = self.calculate_ichimoku_components(self.historical_data)
        
        current_price = data_point['close']
        cloud_top = senkou_a[-1]
        cloud_bottom = senkou_b[-1]

        if current_price > cloud_top and tenkan_sen[-1] > kijun_sen[-1]:
          return 1
        
        return 0

    def should_sell(self, data_point: dict) -> float:
        """Implements the sell logic based on Ichimoku Cloud."""
        if len(self.historical_data) < 52:
          return 0
        
        tenkan_sen, kijun_sen, senkou_a, senkou_b, chikou_span = self.calculate_ichimoku_components(self.historical_data)
        
        current_price = data_point['close']
        cloud_top = senkou_a[-1]
        cloud_bottom = senkou_b[-1]
        if current_price < cloud_bottom and tenkan_sen[-1] < kijun_sen[-1]:
          return 1
        return 0


    def calculate_ichimoku_components(self, data: list) -> tuple[list[float], list[float], list[float], list[float], list[float]]:
        """Calculates all Ichimoku Cloud components."""
        if len(data) < 52:
             if len(data) > 0:
                close_price = data[-1]['close']
                return [close_price], [close_price], [close_price], [close_price], [close_price]
             else:
                 return [0], [0], [0], [0], [0]

        prices = np.array([d['close'] for d in data])
        highs = np.array([d['high'] for d in data])
        lows = np.array([d['low'] for d in data])
        
        tenkan_sen = self._calculate_average(highs, lows, 9)
        kijun_sen = self._calculate_average(highs, lows, 26)
        senkou_a = (tenkan_sen + kijun_sen) / 2
        senkou_b = self._calculate_average(highs, lows, 52)
        chikou_span = prices[-len(senkou_a):]

        return tenkan_sen[-len(senkou_a):], kijun_sen[-len(senkou_a):], senkou_a, senkou_b[-len(senkou_a):], chikou_span

    def _calculate_average(self, highs: np.ndarray, lows: np.ndarray, window: int) -> np.ndarray:
        """Calculates the average of highs and lows over a given window."""
        highest_high = np.zeros_like(highs, dtype=float)
        lowest_low = np.zeros_like(lows, dtype=float)
        
        for i in range(window -1, len(highs)):
            highest_high[i] = np.max(highs[i-window+1:i+1])
            lowest_low[i] = np.min(lows[i-window+1:i+1])

        return (highest_high + lowest_low) / 2

    def update_historical_data(self, data: list):
        """Updates the historical data used by the strategy."""
        self.historical_data = data

    def reset(self):
        """Resets the strategy to its initial state."""
        self.historical_data = []
    
    historical_data = []