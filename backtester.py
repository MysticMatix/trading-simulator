from broker import Broker

class Backtester:
    def __init__(self, initial_balance: float) -> None:
        """Constructor, creates an internal `Broker` instance"""
        self.broker = Broker(initial_balance)

    def run_backtest(self, strategy, data: list) -> dict:
        """Simulates the backtest on given historical data and strategy and returns a dictionary of stats (total profit, number of trades, etc), using an internal `Broker` instance.

        Iterates through each data point, executes the trading strategy, updates balance using `Broker`, and returns stats.
        Keeps track of all trades and results in the internal broker and returns stats
        """
        historical_data = []
        for data_point in data:
            historical_data.append(data_point)
            strategy.update_historical_data(historical_data)
            should_buy = strategy.should_buy(data_point)
            should_sell = strategy.should_sell(data_point)
            print(f"Data point: {data_point}, Buy: {should_buy}, Sell: {should_sell}")
            if should_buy:
                self.broker.execute_trade('buy', 'MSFT', data_point['close'], 1)
            elif should_sell:
               self.broker.execute_trade('sell', 'MSFT', data_point['close'], 1)   

        #Calculate statistics
        final_balance = self.broker.get_balance()
        initial_balance = 10000 #TODO - make it configurable
        profit = final_balance - initial_balance
        trades = len(self.broker.get_transaction_history())
        return {
            'initial_balance': initial_balance,
            'final_balance': final_balance,
            'profit': profit,
            'trades': trades,
            'transaction_history': self.broker.get_transaction_history()
        }
