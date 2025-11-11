import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import datetime


def convert_date_format(date_str):
    # Converts 'DD-MM-YYYY' or "'DD-MM-YYYY'" to 'YYYY-MM-DD'
    date_str = date_str.strip().strip("'")  # remove surrounding quotes if any
    date_obj = datetime.datetime.strptime(date_str, "%d-%m-%Y")
    return date_obj.strftime("%Y-%m-%d")


def predict_stock_price(stock_symbol, start_date, end_date):
    try:
        # Convert dates to correct format
        start_date_fmt = convert_date_format(start_date)
        end_date_fmt = convert_date_format(end_date)

        # Download stock data with auto_adjust=True
        stock_data = yf.download(stock_symbol, start=start_date_fmt, end=end_date_fmt, auto_adjust=True)
        if stock_data.empty:
            return None, "No data found for this symbol and date range."

        stock_data['Date'] = stock_data.index.map(datetime.datetime.toordinal)
        X = stock_data[['Date']]
        y = stock_data['Close']

        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        next_day = datetime.datetime.strptime(end_date_fmt, '%Y-%m-%d') + datetime.timedelta(days=1)
        next_price = model.predict([[next_day.toordinal()]])

        # Convert numpy array to float
        next_price_value = float(next_price[0])

        return (y_test, y_pred, next_day.strftime('%Y-%m-%d'), next_price_value), None

    except Exception as e:
        return None, str(e)


def run_app():
    app = tk.Tk()
    app.title("Stock Market Analyzer and Predictor")
    app.geometry("600x400")

    ttk.Label(app, text="Stock Symbol (e.g., AAPL):").grid(column=0, row=0, padx=10, pady=10)
    symbol_entry = ttk.Entry(app)
    symbol_entry.grid(column=1, row=0, padx=10, pady=10)

    ttk.Label(app, text="Start Date (DD-MM-YYYY):").grid(column=0, row=1, padx=10, pady=10)
    start_date_entry = ttk.Entry(app)
    start_date_entry.grid(column=1, row=1, padx=10, pady=10)

    ttk.Label(app, text="End Date (DD-MM-YYYY):").grid(column=0, row=2, padx=10, pady=10)
    end_date_entry = ttk.Entry(app)
    end_date_entry.grid(column=1, row=2, padx=10, pady=10)

    output_text = tk.Text(app, height=12, width=70)
    output_text.grid(column=0, row=4, columnspan=3, padx=10, pady=10)

    def on_predict():
        symbol = symbol_entry.get().strip().upper()
        start_date = start_date_entry.get().strip()
        end_date = end_date_entry.get().strip()

        if not symbol or not start_date or not end_date:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        result, error = predict_stock_price(symbol, start_date, end_date)
        output_text.delete(1.0, tk.END)
        if error:
            output_text.insert(tk.END, f"Error: {error}")
        else:
            y_test, y_pred, next_day, next_price_value = result
            output_text.insert(tk.END,
                               f"Predicted Close Price for next trading day ({next_day}): ${next_price_value:.2f}\n\n")
            output_text.insert(tk.END, "Actual vs Predicted Close Prices (Sample):\n")
            for actual, pred in zip(list(y_test)[:5], list(y_pred)[:5]):
                output_text.insert(tk.END, f"Actual: ${actual:.2f}, Predicted: ${pred:.2f}\n")

    predict_button = ttk.Button(app, text="Predict", command=on_predict)
    predict_button.grid(column=1, row=3)

    app.mainloop()


if __name__ == "__main__":
    run_app()
