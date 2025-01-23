from strategy import TradingStrategy

class CustomStrategy(TradingStrategy):
    def __init__(self, strategies: list [TradingStrategy], buy_merging_function: callable, sell_merging_function: callable, name:str=None) -> None:
        """Constructor. if weights is None, the strategies will be multiplied instead of averaged."""
        names = [strategy.name for strategy in strategies]
        if name is None:
            name = " + ".join(names)
        super().__init__(name=name)
        self.strategies = strategies
        self.buy_merging_function = buy_merging_function
        self.sell_merging_function = sell_merging_function

    def should_buy(self, data_point: dict) -> float:
        """Implements the buy logic based on the hybrid strategy."""
        scores = [strategy.should_buy(data_point) for strategy in self.strategies]
        return self.buy_merging_function(scores)

    def should_sell(self, data_point: dict) -> float:
        """Implements the sell logic based on the hybrid strategy."""
        scores = [strategy.should_sell(data_point) for strategy in self.strategies]
        return self.sell_merging_function(scores)

    def update_historical_data(self, data: list):
        """Updates the historical data used by the strategy."""
        for strategy in self.strategies:
            strategy.update_historical_data(data)

    def reset(self):
        """Resets the strategy to its default state."""
        for strategy in self.strategies:
            strategy.reset()