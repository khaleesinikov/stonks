import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import requests
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

plt.style.use('bmh')


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
    data = yf.download(tickers, period="max")
    df = pd.DataFrame(data=data)
    print(df.head())
    df["Adj Close"].plot()
    plt.xlabel("Date")
    plt.ylabel("Adjusted Close")
    title_tickers = ", ".join(tickers)
    plt.title(f"Price data for {title_tickers}")
    plt.show()


def make_prediction(ticker):
    data = yf.download(ticker, period="1y")
    df = pd.DataFrame(data=data)
    df = df[["Adj Close"]]
    days = 30
    df["Prediction"] = df[["Adj Close"]].shift(-days)
    x = np.array(df.drop(["Prediction"], 1))[:-days]
    y = np.array(df["Prediction"])[:-days]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
    tree = DecisionTreeRegressor().fit(x_train, y_train)
    x_future = df.drop(["Prediction"], 1)[:-days]
    x_future = x_future.tail(days)
    x_future = np.array(x_future)
    tree_prediction = tree.predict(x_future)
    print(tree_prediction)

    # Plot the tree data
    predictions = tree_prediction
    valid = df[x.shape[0]:]
    valid["Predictions"] = predictions
    ticker = "".join(ticker)
    plt.title(f"Prediction model for {ticker}")
    plt.xlabel("Days", fontsize=18)
    plt.ylabel("Adjusted Close in USD", fontsize=18)
    plt.plot(df["Adj Close"])
    plt.plot(valid[["Adj Close", "Predictions"]])
    plt.legend(["Train", "Val", "Prediction"], loc='lower right')
    plt.show()


symbol = get_ticker()
print(symbol)
if len(symbol) > 1:
    get_data(symbol)
else:
    make_prediction(symbol)
