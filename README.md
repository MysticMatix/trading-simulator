# Algorithmic Trading Simulator

This project is a basic algorithmic trading simulator that allows you to backtest different trading strategies using historical market data. It is designed with a focus on object-oriented programming principles and a modular structure to ensure scalability and maintainability.

## Sources

It currently uses yfinance

## Project Structure

The project consists of the following modules:

*   `data_handler.py`: Fetches, stores, and provides historical market data.
*   `strategies/`: Contains different trading strategies.
   *   `moving_average.py`: Implements a moving average crossover strategy.
   *    `rsi.py`: Implements an RSI based strategy.
   *    `bollinger_bands.py`: Implements a Bollinger bands strategy.
   *    `stochastic_oscillator.py`: Implements a stochastic oscillator strategy. 
   *    `macd.py`: Implements a MACD based strategy.
*   `strategy.py`: Defines the abstract base class for all trading strategies.
*   `broker.py`: Simulates the execution of trades and manages the portfolio.
*   `backtester.py`: Simulates the backtesting process.
*   `main.py`: The entry point of the application.

## How to Use

1.  **Install Dependencies:** Make sure you have all the required packages installed, like yfinance, numpy, etc (run `pip3 install -r requirements.txt` if you have a `requirements.txt` file). Also make sure you have a venv. 
2.  **Run `main.py`:** Execute the `main.py` script using python `python3 main.py` (after activating your virtual environment).
3.  **Modify Parameters:** You can change the parameters of the strategies in `main.py`, by creating new instances of the strategy classes. You can also configure the data that will be backtested.
4.  **Analyze Results:** After running the simulation, the output will display the backtest results, including profit, number of trades, and a transaction history.

## Available Strategies

*   **Moving Average Crossover:** Uses short-term and long-term moving averages to generate buy/sell signals.
*   **RSI:** Uses the Relative Strength Index to identify overbought and oversold conditions.
*   **Bollinger Bands:** Uses Bollinger Bands to identify when a price might be overbought or oversold based on volatility.
*   **Stochastic Oscillator:** Uses the stochastic oscillator to generate signals, based on momentum.
*   **MACD:** Uses the Moving Average Convergence Divergence indicator to generate trading signals, based on the relationship between two moving averages. 

## Further Development

*   Implement more advanced trading strategies.
*   Add more data sources.
*   Include more risk management features.
*   Add visualizations of backtesting results.

