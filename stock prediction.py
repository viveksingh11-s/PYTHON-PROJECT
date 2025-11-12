import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def convert_date_format(date_str):
    try:
        date_str = date_str.strip().strip("'")
        date_obj = datetime.datetime.strptime(date_str, "%d-%m-%Y")
        return date_obj.strftime("%Y-%m-%d")
    except:
        return None

def predict_stock_price(symbol, start, end):
    start = convert_date_format(start)
    end = convert_date_format(end)
    if not start or not end:
        return None, None, None, "Please enter dates as DD-MM-YYYY."

    try:
        data = yf.download(symbol, start=start, end=end, auto_adjust=True)
        if data.empty:
            return None, None, None, "No data available for this symbol and date range."
        data['Date'] = data.index.map(datetime.datetime.toordinal)
        X = data[['Date']]
        y = data['Close']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        if len(y_test) == 0:
            return None, None, None, "Not enough data to predict."
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        next_day = datetime.datetime.strptime(end, '%Y-%m-%d') + datetime.timedelta(days=1)
        next_price = float(model.predict([[next_day.toordinal()]])[0])
        return y_test, y_pred, next_day.strftime('%Y-%m-%d'), next_price
    except Exception as e:
        return None, None, None, str(e)

class StockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stock Market Predictor")
        self.geometry("1000x700")

        ttk.Label(self, text="Stock Symbol (e.g., TCS.NS):").grid(row=0, column=0, padx=10, pady=10)
        self.symbol_entry = ttk.Entry(self)
        self.symbol_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self, text="Start Date (DD-MM-YYYY):").grid(row=1, column=0, padx=10, pady=10)
        self.start_date_entry = ttk.Entry(self)
        self.start_date_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self, text="End Date (DD-MM-YYYY):").grid(row=2, column=0, padx=10, pady=10)
        self.end_date_entry = ttk.Entry(self)
        self.end_date_entry.grid(row=2, column=1, padx=10, pady=10)

        self.output_text = tk.Text(self, height=12, width=110)
        self.output_text.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        self.fig = Figure(figsize=(8, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        self.predict_button = ttk.Button(self, text="Predict", command=self.on_predict)
        self.predict_button.grid(row=5, column=1, pady=20)

    def on_predict(self):
        self.output_text.delete(1.0, tk.END)
        self.ax.clear()

        symbol = self.symbol_entry.get().strip().upper()
        start_date = self.start_date_entry.get().strip()
        end_date = self.end_date_entry.get().strip()

        if not symbol or not start_date or not end_date:
            messagebox.showerror("Input Error", "Please fill all fields.")
            self.canvas.draw_idle()
            return

        y_test, y_pred, next_day, next_price = predict_stock_price(symbol, start_date, end_date)

        if y_test is None or y_pred is None:
            self.output_text.insert(tk.END, f"Error: {next_price}\n")
            self.ax.text(0.5, 0.5, "No data to plot", ha='center', fontsize=14)
            self.canvas.draw_idle()
            return

        self.output_text.insert(tk.END, f"Predicted Close Price for next trading day ({next_day}): ${next_price:.2f}\n\n")
        self.output_text.insert(tk.END, "Sample Actual vs Predicted Close Prices:\n")

        samples = min(10, len(y_test))
        actuals = y_test.tolist()[:samples]
        preds = y_pred.tolist()[:samples]

        for i in range(samples):
            self.output_text.insert(tk.END, f"Actual: ${actuals[i]:.2f}, Predicted: ${preds[i]:.2f}\n")

        x_vals = list(range(samples))
        self.ax.plot(x_vals, actuals, label="Actual", marker='o', color='blue')
        self.ax.plot(x_vals, preds, label="Predicted", marker='x', color='red')
        self.ax.set_title(f"{symbol} Close Price Prediction Sample")
        self.ax.set_xlabel("Sample Index")
        self.ax.set_ylabel("Close Price")
        self.ax.legend()
        self.ax.grid(True)

        self.canvas.draw_idle()

if __name__ == "__main__":
    app = StockApp()
    app.mainloop()
