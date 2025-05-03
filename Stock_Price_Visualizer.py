import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# Get user input with validation
while True:
    ticker = input("Enter a stock ticker symbol (e.g., AAPL): ").upper()
    if ticker.isalpha():
        break
    print("❌ Invalid ticker. Please enter alphabetic characters only.")

while True:
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    if not (is_valid_date(start_date) and is_valid_date(end_date)):
        print("❌ Invalid date format. Please use YYYY-MM-DD.")
        continue

    if start_date >= end_date:
        print("❌ Start date must be before end date.")
        continue

    break

# Try downloading data
try:
    data = yf.download(ticker, start=start_date, end=end_date)

    if data.empty:
        print(f"⚠️ No data found for {ticker} in that date range.")
    else:
        data['SMA_20'] = data['Close'].rolling(window=20).mean()
        data['SMA_50'] = data['Close'].rolling(window=50).mean()

        plt.figure(figsize=(10, 5))
        plt.plot(data['Close'], label='Close Price')
        plt.plot(data['SMA_20'], label='20-Day MA')
        plt.plot(data['SMA_50'], label='50-Day MA')
        plt.title(f"{ticker} with Moving Averages")
        plt.xlabel("Date")
        plt.ylabel("Price ($)")
        plt.legend()
        plt.grid(True)
        plt.show()

except Exception as e:
    print(f"❌ An error occurred while fetching data: {e}")
