
class Broker:
    def __init__(self, initial_balance: float) -> None:
        """Constructor."""
        self.balance = initial_balance
        self.portfolio = {}
        self.transaction_history = []

    def execute_trade(self, trade_type: str, symbol: str, price: float, volume: float) -> bool:
        """Simulates the execution of a trade, returns True if success, False if failed, logs the transaction in the `transaction_history`.

        Handles buying, selling, and insufficient funds cases.
        """
        if trade_type == 'buy':
            cost = price * volume
            if self.balance >= cost:
                self.balance -= cost
                if symbol in self.portfolio:
                  self.portfolio[symbol] += volume
                else:
                  self.portfolio[symbol] = volume
                self.transaction_history.append({
                    'time': 'now',  # Placeholder for actual time
                    'type': 'buy',
                    'symbol': symbol,
                    'price': price,
                    'volume': volume,
                    'status': 'success'
                })
                return True
            else:
                self.transaction_history.append({
                    'time': 'now',  # Placeholder for actual time
                    'type': 'buy',
                    'symbol': symbol,
                    'price': price,
                    'volume': volume,
                    'status': 'failure (insufficient funds)'
                })
                return False
        elif trade_type == 'sell':
          if symbol in self.portfolio and self.portfolio[symbol] >= volume:
            self.balance += price * volume
            self.portfolio[symbol] -= volume
            self.transaction_history.append({
                'time': 'now',  # Placeholder for actual time
                'type': 'sell',
                'symbol': symbol,
                'price': price,
                'volume': volume,
                'status': 'success'
            })
            return True
          else:
            self.transaction_history.append({
                'time': 'now',  # Placeholder for actual time
                'type': 'sell',
                'symbol': symbol,
                'price': price,
                'volume': volume,
                 'status': 'failure (not enough assets)'
            })
            return False
        return False

    def get_balance(self) -> float:
        """Returns current balance."""
        return self.balance

    def get_portfolio(self) -> dict:
        """Returns current portfolio."""
        return self.portfolio

    def get_transaction_history(self) -> list:
        """Returns transaction history"""
        return self.transaction_history
