from strategy import TradingStrategy
import numpy as np

class ADXStrategy(TradingStrategy):
    def __init__(self, period: int = 14) -> None:
        """Constructor."""
        super().__init__(name="ADX Strategy")
        self.period = period

    def should_buy(self, data_point: dict) -> float:
        """Implements the buy logic based on ADX and DMI."""
        if len(self.historical_data) < self.period + 1:
            return 0

        adx, pdi, mdi = self.calculate_adx(self.historical_data)

        if adx[-1] > 25 and pdi[-1] > mdi[-1]:
            return 1
        return 0

    def should_sell(self, data_point: dict) -> float:
        """Implements the sell logic based on ADX and DMI."""
        if len(self.historical_data) < self.period + 1:
            return 0
        
        adx, pdi, mdi = self.calculate_adx(self.historical_data)

        if adx[-1] > 25 and mdi[-1] > pdi[-1]:
            return 1
        return 0

    def calculate_adx(self, data: list) -> tuple[list[float], list[float], list[float]]:
        """Calculates the ADX, +DI, and -DI for the given data list."""
        if len(data) < self.period + 1:
            if len(data) > 0:
                close_price = data[-1]['close']
                return [close_price], [close_price], [close_price]
            else:
                return [0], [0], [0]

        prices = np.array([d['close'] for d in data])
        highs = np.array([d['high'] for d in data])
        lows = np.array([d['low'] for d in data])

        tr = np.zeros(len(data))
        pdm = np.zeros(len(data))
        mdm = np.zeros(len(data))

        for i in range(1, len(data)):
            tr[i] = max(highs[i] - lows[i], abs(highs[i] - prices[i-1]), abs(lows[i] - prices[i-1]))
            pdm[i] = highs[i] - highs[i-1] if (highs[i] - highs[i-1]) > (lows[i-1] - lows[i]) else 0
            mdm[i] = lows[i-1] - lows[i] if (lows[i-1] - lows[i]) > (highs[i] - highs[i-1]) else 0

        atr = self._calculate_smoothed_values(tr, self.period)
        pdm_smooth = self._calculate_smoothed_values(pdm, self.period)
        mdm_smooth = self._calculate_smoothed_values(mdm, self.period)

        pdi = (pdm_smooth / atr) * 100
        mdi = (mdm_smooth / atr) * 100

        dx = np.abs((pdi - mdi) / (pdi + mdi)) * 100
        adx = self._calculate_smoothed_values(dx, self.period)
        
        return adx[-len(pdi):], pdi[-len(pdi):], mdi[-len(mdi):]

    def _calculate_smoothed_values(self, data: np.ndarray, window: int) -> np.ndarray:
        """Calculates the smoothed moving average of the input array"""
        smoothed_values = np.zeros_like(data, dtype=float)
        smoothed_values[:window] = np.mean(data[:window])
        alpha = 1/window
        for i in range(window, len(data)):
            smoothed_values[i] = alpha * data[i] + (1 - alpha) * smoothed_values[i-1]
        return smoothed_values

    def update_historical_data(self, data: list):
        """Updates the historical data used by the strategy."""
        self.historical_data = data

    def reset(self):
        """Resets the strategy to its initial state."""
        self.historical_data = []

    historical_data = []