from broker import Broker

class Backtester:
    def __init__(self, initial_balance: float) -> None:
        """Constructor, creates an internal `Broker` instance"""
        self.broker = Broker(initial_balance)

    def run_backtest(self, strategy, data: list, symbol="ABCDEF", multiplier = 10) -> dict:
        """Simulates the backtest on given historical data and strategy and returns a dictionary of stats (total profit, number of trades, etc), using an internal `Broker` instance.

        Iterates through each data point, executes the trading strategy, updates balance using `Broker`, and returns stats.
        Keeps track of all trades and results in the internal broker and returns stats
        """
        historical_data = []
        for i, data_point in enumerate(data):
            historical_data.append(data_point)
            strategy.update_historical_data(historical_data)
            should_buy = strategy.should_buy(data_point)
            should_sell = strategy.should_sell(data_point)
            #print(f"{i}: Data point: {data_point}, Buy: {should_buy}, Sell: {should_sell}")
            if should_buy > 0:
                self.broker.execute_trade('buy', symbol, data_point['close'], multiplier * should_buy // 1)
            elif should_sell > 0:
               self.broker.execute_trade('sell', symbol, data_point['close'], multiplier * should_sell // 1)

        #Calculate statistics
        final_balance = self.broker.get_balance()
        initial_balance = 10000 #TODO - make it configurable
        profit = final_balance - initial_balance
        trades = len(self.broker.get_transaction_history())

        #current value of owned stocks:
        stock_price = data[-1]['close']
        owned_stocks = self.broker.portfolio[symbol]
        stock_value = owned_stocks * stock_price

        final_balance_with_stocks = final_balance + stock_value
        profit_with_stocks = final_balance_with_stocks - initial_balance

        return {
            'initial_balance': initial_balance,
            'final_balance': final_balance,
            'final_balance_with_stocks': final_balance_with_stocks,
            'profit': profit,
            'profit_with_stocks': profit_with_stocks,
            'trades': trades,
            'transaction_history': self.broker.get_transaction_history()
        }
