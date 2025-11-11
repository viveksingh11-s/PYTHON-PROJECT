import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import DateEntry

def predict_stock_price(stock_symbol, start_date, end_date):
    try:
        stock_data = yf.download(stock_symbol, start=start_date, end=end_date, auto_adjust=True, progress=False)
        if stock_data.empty:
            return None, None, None, "No data found for this symbol or date range."
        stock_data['Date'] = stock_data.index.map(datetime.datetime.toordinal)
        X = stock_data[['Date']]
        y = stock_data['Close']
        if len(X) < 2:
            return None, None, None, "Not enough data for prediction. Try broader range."
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        if len(y_test) == 0:
            return None, None, None, "Not enough data in test sample. Try broader range."
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        next_day = datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1)
        next_price = float(model.predict([[next_day.toordinal()]])[0])
        return y_test, y_pred, next_day.strftime('%Y-%m-%d'), next_price
    except Exception as e:
        return None, None, None, str(e)

class StockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stock Market Analyzer and Predictor")
        self.geometry("1100x750")
        self.configure(bg="#f5f7fa")

        ttk.Label(self, text="Stock Symbol (e.g., TCS.NS):", font=('Arial', 12)).grid(row=0, column=0, padx=15, pady=12, sticky='e')
        self.symbol_entry = ttk.Entry(self, font=('Arial', 12))
        self.symbol_entry.grid(row=0, column=1, padx=15, pady=12, sticky='w')

        ttk.Label(self, text="Start Date:", font=('Arial', 12)).grid(row=1, column=0, padx=15, pady=12, sticky='e')
        self.start_cal = DateEntry(self, date_pattern='yyyy-mm-dd', font=('Arial', 12), background='darkblue', foreground='white', borderwidth=2)
        self.start_cal.grid(row=1, column=1, padx=15, pady=12, sticky='w')

        ttk.Label(self, text="End Date:", font=('Arial', 12)).grid(row=2, column=0, padx=15, pady=12, sticky='e')
        self.end_cal = DateEntry(self, date_pattern='yyyy-mm-dd', font=('Arial', 12), background='darkblue', foreground='white', borderwidth=2)
        self.end_cal.grid(row=2, column=1, padx=15, pady=12, sticky='w')

        self.predict_button = ttk.Button(self, text="Predict", command=self.on_predict)
        self.predict_button.grid(row=3, column=1, pady=20, sticky='w')

        self.clear_button = ttk.Button(self, text="Clear", command=self.on_clear)
        self.clear_button.grid(row=3, column=1, padx=120, pady=20, sticky='w')

        self.output_text = tk.Text(self, height=10, width=110, font=('Consolas', 11))
        self.output_text.grid(row=4, column=0, columnspan=3, padx=20, pady=12)

        self.fig = Figure(figsize=(10, 5), dpi=100, facecolor='#f5f7fa')
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=5, column=0, columnspan=3, padx=20, pady=20)

    def on_clear(self):
        self.output_text.delete(1.0, tk.END)
        self.ax.clear()
        self.ax.set_facecolor("#fafafa")
        self.canvas.draw_idle()

    def on_predict(self):
        self.output_text.delete(1.0, tk.END)
        self.ax.clear()
        self.ax.set_facecolor("#fafafa")
        symbol = self.symbol_entry.get().strip().upper()
        start_date = self.start_cal.get_date().strftime('%Y-%m-%d')
        end_date = self.end_cal.get_date().strftime('%Y-%m-%d')

        if not symbol:
            messagebox.showerror("Input Error", "Please enter the stock symbol.")
            self.canvas.draw_idle()
            return

        y_test, y_pred, next_day, next_price_value = predict_stock_price(symbol, start_date, end_date)
        if y_test is None or y_pred is None:
            self.output_text.insert(tk.END, f"{next_price_value}\n")
            self.ax.text(0.5, 0.5, "No predicted graph data", ha='center', fontsize=16, color="red")
            self.canvas.draw_idle()
            return

        self.output_text.insert(tk.END, f"Predicted Close Price for next trading day ({next_day}): ${next_price_value:.2f}\n\n")

        if len(y_test) == 0:
            self.output_text.insert(tk.END, "Actual vs Predicted Close Prices (Sample):\n")
            self.output_text.insert(tk.END, "Not enough data in test sample. Pick a wider date range.\n")
            self.ax.text(0.5, 0.5, "No data for test sample.\nTry a wider date range.", ha='center', fontsize=12, color="red")
            self.canvas.draw_idle()
            return

        self.output_text.insert(tk.END, "Actual vs Predicted Close Prices (Sample):\n")
        samples = min(10, len(y_test))
        actuals = y_test.tolist()[:samples]
        preds = y_pred.tolist()[:samples]
        for i in range(samples):
            self.output_text.insert(tk.END, f"Actual: ${actuals[i]:.2f}, Predicted: ${preds[i]:.2f}\n")

        x_vals = list(range(samples))
        self.ax.plot(x_vals, actuals, label="Actual", marker='o', linestyle='-', color='#004488', linewidth=2, markersize=8)
        self.ax.plot(x_vals, preds, label="Predicted", marker='x', linestyle='--', color='#ef233c', linewidth=2, markersize=10)
        self.ax.set_title(f"{symbol} Close Price Prediction (Sample)", fontsize=14, color='#002244', fontweight='bold')
        self.ax.set_xlabel("Sample Index", fontsize=12)
        self.ax.set_ylabel("Close Price", fontsize=12)
        self.ax.legend()
        self.ax.grid(True, which='both', linestyle=':', linewidth=1, color='#aaa')
        self.canvas.draw_idle()

if __name__ == "__main__":
    app = StockApp()
    app.mainloop()
