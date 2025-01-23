from strategy import TradingStrategy
import numpy as np

class StochasticOscillatorStrategy(TradingStrategy):
    def __init__(self, period: int, overbought: int = 80, oversold: int = 20) -> None:
        """Constructor."""
        super().__init__(name="Stochastic Oscillator Strategy")
        self.period = period
        self.overbought = overbought
        self.oversold = oversold

    def should_buy(self, data_point: dict) -> float:
        """Implements the buy logic based on Stochastic Oscillator."""
        if len(self.historical_data) < self.period:
            return 0

        k_values, d_values = self.calculate_stochastic_oscillator(self.historical_data)

        if len(k_values) < 2 or len(d_values) < 2:
            return 0

        if k_values[-1] < self.oversold and k_values[-1] > d_values[-1] and k_values[-2] <= d_values[-2]:
          return 1
        return 0


    def should_sell(self, data_point: dict) -> float:
        """Implements the sell logic based on Stochastic Oscillator."""
        if len(self.historical_data) < self.period:
             return 0

        k_values, d_values = self.calculate_stochastic_oscillator(self.historical_data)

        if len(k_values) < 2 or len(d_values) < 2:
            return 0

        if k_values[-1] > self.overbought and k_values[-1] < d_values[-1] and k_values[-2] >= d_values[-2]:
          return 1
        return 0
    
    def calculate_stochastic_oscillator(self, data: list) -> tuple[list[float], list[float]]:
        """Calculates the Stochastic Oscillator (%K and %D) for the given data list."""
        if len(data) < self.period:
            if len(data) > 0:
                close_price = data[-1]['close']
                return [close_price], [close_price]
            else:
              return [0], [0]
        
        prices = np.array([d['close'] for d in data[-self.period:]])
        highest_high = np.max([d['high'] for d in data[-self.period:]])
        lowest_low = np.min([d['low'] for d in data[-self.period:]])

        k_values = []
        for i in range(self.period, len(data)):
            current_close = data[i]['close']
            k = ((current_close - lowest_low) / (highest_high - lowest_low)) * 100
            k_values.append(k)

        d_values = []
        for i in range(2, len(k_values)):
            d_values.append(np.mean(k_values[i-2:i+1]))
        
        if len(k_values) > 0 and len(d_values) == 0:
          d_values = [k_values[-1]]
          
        return k_values, d_values

    def update_historical_data(self, data: list):
        """Updates the historical data used by the strategy."""
        self.historical_data = data

    def reset(self):
        """Resets the strategy to its default state
        (no historical data and no previous moving averages)."""
        self.historical_data = []

        
    historical_data = []