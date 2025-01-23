from strategy import TradingStrategy
import numpy as np

class RSIStrategy(TradingStrategy):
    def __init__(self, period: int, overbought: int = 70, oversold: int = 30) -> None:
        """Constructor."""
        super().__init__(name="RSI Strategy")
        self.period = period
        self.overbought = overbought
        self.oversold = oversold
        self.historical_data = []

    def should_buy(self, data_point: dict) -> float:
        """Implements the buy logic based on RSI."""
        if len(self.historical_data) < self.period + 1:
            return 0

        rsi = self.calculate_rsi(self.historical_data)
        if rsi < self.oversold:
            return 1
        return 0

    def should_sell(self, data_point: dict) -> float:
        """Implements the sell logic based on RSI."""
        if len(self.historical_data) < self.period + 1:
            return 0

        rsi = self.calculate_rsi(self.historical_data)
        if rsi > self.overbought:
            return 1
        return 0

    def calculate_rsi(self, data: list) -> float:
        """Calculates the RSI for the given data list."""
        if len(data) < self.period + 1:
            return 50  # neutral value

        prices = np.array([d['close'] for d in data[-self.period - 1:]])
        deltas = np.diff(prices)
        gains = deltas.copy()
        losses = deltas.copy()
        gains[gains < 0] = 0
        losses[losses > 0] = 0
        losses = np.abs(losses)

        avg_gain = np.mean(gains[1:])
        avg_loss = np.mean(losses[1:])

        if avg_loss == 0:
            return 100

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def update_historical_data(self, data: list):
        """Updates the historical data used by the strategy."""
        self.historical_data = data

    def reset(self):
        """Resets the strategy."""
        self.historical_data = []
