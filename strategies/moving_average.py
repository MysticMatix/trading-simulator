from strategy import TradingStrategy

class MovingAverageStrategy(TradingStrategy):
    def __init__(self, short_window: int, long_window: int) -> None:
        """Constructor."""
        super().__init__(name="Moving Average Strategy")
        self.short_window = short_window
        self.long_window = long_window

    def should_buy(self, data_point: dict) -> bool:
        """Implements the buy logic based on moving averages."""
        if len(self.historical_data) < self.long_window:
            return 0
        short_ma = self.calculate_moving_average(self.historical_data, self.short_window)
        long_ma = self.calculate_moving_average(self.historical_data, self.long_window)

        # print(f"  Short MA: {short_ma}, Long MA: {long_ma}, Prev Short MA: {self.prev_short_ma}, Prev Long MA: {self.prev_long_ma}")

        if short_ma > long_ma and self.prev_short_ma <= self.prev_long_ma:
            self.prev_short_ma = short_ma
            self.prev_long_ma = long_ma
            return 1
        else:
            self.prev_short_ma = short_ma
            self.prev_long_ma = long_ma
            return 0

    def should_sell(self, data_point: dict) -> bool:
        """Implements the sell logic based on moving averages."""
        if len(self.historical_data) < self.long_window:
            return 0
        short_ma = self.calculate_moving_average(self.historical_data, self.short_window)
        long_ma = self.calculate_moving_average(self.historical_data, self.long_window)

        # print(f"  Short MA: {short_ma}, Long MA: {long_ma}, Prev Short MA: {self.prev_short_ma}, Prev Long MA: {self.prev_long_ma}")

        if short_ma < long_ma and self.prev_short_ma >= self.prev_long_ma:
            self.prev_short_ma = short_ma
            self.prev_long_ma = long_ma
            return 1
        else:
           self.prev_short_ma = short_ma
           self.prev_long_ma = long_ma
           return 0

    def calculate_moving_average(self, data: list, window: int) -> float:
        """Calculates the moving average for a given data list."""
        if len(data) < window:
           if len(data) > 0:
              # print(f"  Not enough data to calculate MA, data length: {len(data)}, window: {window}, returning last price: {data[-1]['close']}")
              return data[-1]['close']
           else:
              # print(f"  Not enough data to calculate MA, data length: {len(data)}, window: {window}, returning 0")
              return 0
        prices = [d['close'] for d in data[-window:]]
        ma = sum(prices) / window
        return ma
    
    def update_historical_data(self, data: list):
        self.historical_data = data

    historical_data = []
    prev_short_ma = 0
    prev_long_ma = 0