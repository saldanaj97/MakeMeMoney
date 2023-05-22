import yfinance as yf 

# Function to gather stock info
def gatherStockHistory(symbol, period):
    stock = yf.Ticker(symbol)
    stock.info
    hist = stock.history(period=period)
    return hist

print(gatherStockHistory('IBM', '1mo'))
