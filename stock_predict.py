import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import requests


def check_if_valid_ticker(ticker):
    url = f"http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={ticker}&region=1&lang=en"
    result = requests.get(url).json()
    try:
        if result['ResultSet']['Result'][0]['symbol'] != ticker:
            return False
        else:
            return True
    except IndexError:
        return False


def get_ticker(flag=False):
    while not flag:
        ticker_list = list(dict.fromkeys(input(f"Enter valid ticker(s): ").upper().split()))  # clear duplicates
        for ticker in list(ticker_list):
            if not check_if_valid_ticker(ticker):
                ticker_list.remove(ticker)
                print(f"{ticker} was not found.")
        if ticker_list:
            return ticker_list


def get_data(tickers):
    data = yf.download(tickers, period="1y")
    df = pd.DataFrame(data=data)
    print(df.head())
    df["Adj Close"].plot()
    plt.xlabel("Date")
    plt.ylabel("Adjusted Close")
    title_tickers = ", ".join(tickers)
    plt.title(f"Price data for {title_tickers}")
    plt.show()


symbol = get_ticker()
print(symbol)
get_data(symbol)
