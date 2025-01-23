from strategy import TradingStrategy
import numpy as np

class HybridStrategy(TradingStrategy):
    def __init__(self, strategies: list[TradingStrategy], weights: list[float] | None, name:str=None) -> None:
        """Constructor. if weights is None, the strategies will be multiplied instead of averaged."""
        names = [strategy.name for strategy in strategies]
        if name is None:
            name = " + ".join(names)
        super().__init__(name=name)
        self.strategies = strategies
        self.weights = weights

    def should_buy(self, data_point: dict) -> float:
        """Implements the buy logic based on the hybrid strategy."""
        scores = [strategy.should_buy(data_point) for strategy in self.strategies]
        if self.weights is None:
            return np.prod(scores)
        return np.average(scores, weights=self.weights)

    def should_sell(self, data_point: dict) -> float:
        """Implements the sell logic based on the hybrid strategy."""
        scores = [strategy.should_sell(data_point) for strategy in self.strategies]
        if self.weights is None:
            return np.prod(scores)
        return np.average(scores, weights=self.weights)
    
    def update_historical_data(self, data: list):
        """Updates the historical data used by the strategy."""
        for strategy in self.strategies:
            strategy.update_historical_data(data)

    def reset(self):
        """Resets the strategy to its default state."""
        for strategy in self.strategies:
            strategy.reset()