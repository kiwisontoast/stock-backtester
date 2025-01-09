import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import sv_ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class StockBacktestApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Stock Portfolio Backtesting App")
        self.master.geometry("800x600")
        # Add the protocol handler here
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        sv_ttk.set_theme("light")  # Initialize with light theme
        self.create_widgets()

    def on_closing(self):
        plt.close('all')  # Close all matplotlib figures
        self.master.quit()  # Stop the mainloop
        self.master.destroy()  # Destroy the window
        
    def toggle_theme(self):
        new_theme = self.theme_var.get()
        sv_ttk.set_theme(new_theme)
        
        # Update plot colors
        if new_theme == "dark":
            self.fig.patch.set_facecolor('#2d2d2d')
            self.ax.set_facecolor('#2d2d2d')
            self.ax.tick_params(colors='white')
            self.ax.xaxis.label.set_color('white')
            self.ax.yaxis.label.set_color('white')
            self.ax.title.set_color('white')
        else:
            self.fig.patch.set_facecolor('white')
            self.ax.set_facecolor('white')
            self.ax.tick_params(colors='black')
            self.ax.xaxis.label.set_color('black')
            self.ax.yaxis.label.set_color('black')
            self.ax.title.set_color('black')
        
        self.canvas.draw()



    def create_widgets(self):
        # Date selection
        ttk.Label(self.master, text="Start Date:").grid(row=0, column=0, padx=5, pady=5)
        self.start_date = DateEntry(self.master, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.start_date.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.master, text="End Date:").grid(row=0, column=2, padx=5, pady=5)
        self.end_date = DateEntry(self.master, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.end_date.grid(row=0, column=3, padx=5, pady=5)

        # Stock input
        ttk.Label(self.master, text="Stock Tickers (comma-separated):").grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        self.stock_entry = ttk.Entry(self.master, width=30)
        self.stock_entry.grid(row=1, column=2, columnspan=2, padx=5, pady=5)

        # Theme toggle switch
        self.theme_var = tk.StringVar(value="light")
        self.theme_switch = ttk.Checkbutton(
            self.master,
            text="Dark Mode",
            style="Switch.TCheckbutton",
            variable=self.theme_var,
            onvalue="dark",
            offvalue="light",
            command=self.toggle_theme
        )
        self.theme_switch.grid(row=8, column=0, columnspan=4, pady=10)

        # Allocation type
        self.allocation_type = tk.StringVar(value="percentage")
        ttk.Radiobutton(self.master, text="Percentage", variable=self.allocation_type, value="percentage").grid(row=2, column=0, padx=5, pady=5)
        ttk.Radiobutton(self.master, text="Dollar Amount", variable=self.allocation_type, value="dollar").grid(row=2, column=1, padx=5, pady=5)

        # Allocation input
        ttk.Label(self.master, text="Allocations:").grid(row=3, column=0, padx=5, pady=5)
        self.allocation_entry = ttk.Entry(self.master, width=30)
        self.allocation_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

        # Baseline stock
        ttk.Label(self.master, text="Baseline Stock:").grid(row=4, column=0, padx=5, pady=5)
        self.baseline_entry = ttk.Entry(self.master, width=10)
        self.baseline_entry.grid(row=4, column=1, padx=5, pady=5)

        # Run button
        ttk.Button(self.master, text="Run Backtest", command=self.run_backtest).grid(row=5, column=0, columnspan=4, pady=10)

        # Results area
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

        self.results_text = tk.Text(self.master, height=5, width=80)
        self.results_text.grid(row=7, column=0, columnspan=4, padx=10, pady=10)

    def run_backtest(self):
        try:
            start_date = self.start_date.get_date()
            end_date = self.end_date.get_date()
            stocks = [s.strip() for s in self.stock_entry.get().split(',')]
            baseline_stock = self.baseline_entry.get().strip()
            allocation_type = self.allocation_type.get()
            allocations = [float(a.strip()) for a in self.allocation_entry.get().split(',')]

            # Verify input data lengths match
            if len(stocks) != len(allocations):
                messagebox.showerror("Error", "Number of stocks must match number of allocations")
                return

            # Fetch stock data first
            portfolio_data = yf.download(stocks + [baseline_stock], start=start_date, end=end_date, auto_adjust=False)
            
            # Use 'Close' for calculations, but keep 'Adj Close' for total return
            close_data = portfolio_data['Close']
            adj_close_data = portfolio_data['Adj Close']

            # Calculate portfolio value and weights
            if allocation_type == "percentage":
                if sum(allocations) != 100:
                    messagebox.showerror("Error", "Percentage allocations must sum to 100%")
                    return
                weights = [a / 100 for a in allocations]
                portfolio_value = pd.Series(0, index=close_data.index)
                for stock, weight in zip(stocks, weights):
                    portfolio_value += close_data[stock] * weight
            else:  # dollar amount
                total_investment = sum(allocations)
                weights = [a / total_investment for a in allocations]
                portfolio_value = pd.Series(0, index=close_data.index)
                for stock, allocation in zip(stocks, allocations):
                    shares = allocation / close_data[stock].iloc[0]
                    portfolio_value += close_data[stock] * shares

            # Calculate returns
            portfolio_return = sum((adj_close_data[stock].iloc[-1] / adj_close_data[stock].iloc[0] - 1) * weight 
                                for stock, weight in zip(stocks, weights)) * 100
            baseline_return = (adj_close_data[baseline_stock].iloc[-1] / adj_close_data[baseline_stock].iloc[0] - 1) * 100

            # Plot results
            self.ax.clear()
            self.ax.plot(portfolio_value.index, portfolio_value / portfolio_value.iloc[0], label='Portfolio')
            self.ax.plot(close_data.index, close_data[baseline_stock] / close_data[baseline_stock].iloc[0], 
                        label=baseline_stock)
            self.ax.set_title('Portfolio Performance vs Baseline')
            self.ax.set_xlabel('Date')
            self.ax.set_ylabel('Normalized Value')
            self.ax.legend()
            self.canvas.draw()

            # Display results
            self.results_text.delete('1.0', tk.END)
            self.results_text.insert(tk.END, f"Portfolio Return: {portfolio_return:.2f}%\n")
            self.results_text.insert(tk.END, f"Baseline Return ({baseline_stock}): {baseline_return:.2f}%\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = StockBacktestApp(root)
    root.mainloop()

