from abc import ABC, abstractmethod

class TradingStrategy(ABC):
    def __init__(self, name: str) -> None:
        """Constructor."""
        self.name = name

    @abstractmethod
    def should_buy(self, data_point: dict) -> float:
        """Abstract method, returns the buy signal based on the strategy. Should return a float value between 0 and 1."""
        pass

    @abstractmethod
    def should_sell(self, data_point: dict) -> int:
        """Abstract method, returns the sell signal based on the strategy. Should return a float value between 0 and 1."""
        pass

    @abstractmethod
    def update_historical_data(self, data: list):
        """Abstract method, updates the historical data used by the strategy."""
        pass

    @abstractmethod
    def reset(self):
        """Abstract method, resets the strategy."""
        pass