import yfinance as yf
import pandas as pd
from pandas_datareader import data as pdr

# Download data from yfinance while making sure data is formatted correctly
yf.pdr_override()

# Set display options to show all columns and rows
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.expand_frame_repr", False)


# Function to gather stock info
def gatherStockData(symbol, start_date, end_date):
    # Fetch historical data
    data = pdr.get_data_yahoo(symbol, start=start_date, end=end_date)

    # Calculate moving averages
    data["50-day MA"] = data["Close"].rolling(window=50).mean()
    data["200-day MA"] = data["Close"].rolling(window=200).mean()

    return data


# Function to help generate buy signal (50-day MA crosses above 200-day MA)
def generateBuySignal(symbol, start_date, end_date):
    # Gather stock data
    data = gatherStockData(symbol, start_date, end_date)

    # Find when 50-day MA crosses above 200-day MA and when the signal changes indicating a buy signal
    data["BuySignal"] = 0

    # Create a numerical index col to avoid errors with slice indexing on DatetimeIndex
    data["numerical_index"] = range(len(data))
    data.loc[data["numerical_index"] >= 50, "BuySignal"] = (
        data.loc[data["numerical_index"] >= 50, "50-day MA"] > data.loc[data["numerical_index"] >= 50, "200-day MA"]
    )
    data["BuyPosition"] = data["BuySignal"].diff()

    # Store and return date of the buy signal
    buy_date = data[data["BuyPosition"] == 1].index[0] if len(data[data["BuyPosition"] == 1]) > 0 else None
    return buy_date


# Function to help generate sell signal (50-day MA crosses below 200-day MA) (comments are same as generateBuySignal except for a sell signal)
def generateSellSignal(symbol, start_date, end_date):
    data = gatherStockData(symbol, start_date, end_date)
    data["SellSignal"] = 0
    data["numerical_index"] = range(len(data))
    data.loc[data["numerical_index"] >= 50, "SellSignal"] = (
        data.loc[data["numerical_index"] >= 50, "50-day MA"] < data.loc[data["numerical_index"] >= 50, "200-day MA"]
    )
    data["SellPosition"] = data["SellSignal"].diff()
    sell_date = data[data["SellPosition"] == 1].index[0] if len(data[data["SellPosition"] == 1]) > 0 else None
    return sell_date


def main():
    # Define stock symbol and time period
    symbol = "AAPL"
    start_date = "2022-01-01"
    end_date = "2023-05-23"
    buy_date = generateBuySignal(symbol, start_date, end_date)
    sell_date = generateSellSignal(symbol, start_date, end_date)
    print("Buy: ", buy_date)
    print("Sell: ", sell_date)


if __name__ == "__main__":
    main()
