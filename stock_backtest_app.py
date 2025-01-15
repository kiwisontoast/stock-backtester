import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import sv_ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests


class StockBacktestApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Stock Portfolio Backtesting App")
        self.master.geometry("800x1000")

        plt.rcParams.update(
            {
                "text.color": "white",
                "axes.labelcolor": "white",
                "axes.edgecolor": "white",
                "xtick.color": "white",
                "ytick.color": "white",
                "figure.facecolor": "black",
                "axes.facecolor": "black",
            }
        )

        self.current_config = {}

        self.master.grid_rowconfigure(6, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)
        self.master.grid_columnconfigure(3, weight=1)

        self.master.configure(padx=10, pady=10)
        self.master.minsize(800, 1000)

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        sv_ttk.set_theme("dark")
        self.create_widgets()
        self.update_graph_colors()

    def update_graph_colors(self):
        if self.theme_var.get() == "dark":
            self.fig.patch.set_facecolor("#2d2d2d")
            self.ax.set_facecolor("#2d2d2d")
            self.ax.tick_params(colors="white")
            self.ax.xaxis.label.set_color("white")
            self.ax.yaxis.label.set_color("white")
            self.ax.title.set_color("white")
        self.canvas.draw()

    def on_closing(self):
        plt.close("all")
        self.master.quit()
        self.master.destroy()

    def toggle_theme(self):
        new_theme = self.theme_var.get()
        sv_ttk.set_theme(new_theme)

        if new_theme == "dark":
            self.fig.patch.set_facecolor("#2d2d2d")
            self.ax.set_facecolor("#2d2d2d")
            self.ax.tick_params(colors="white")
            self.ax.xaxis.label.set_color("white")
            self.ax.yaxis.label.set_color("white")
            self.ax.title.set_color("white")
        else:
            self.fig.patch.set_facecolor("white")
            self.ax.set_facecolor("white")
            self.ax.tick_params(colors="black")
            self.ax.xaxis.label.set_color("black")
            self.ax.yaxis.label.set_color("black")
            self.ax.title.set_color("black")

        self.canvas.draw()

    def create_widgets(self):
        ttk.Label(self.master, text="Start Date:").grid(row=0, column=0, padx=5, pady=5)
        graph_frame = ttk.Frame(self.master)
        graph_frame.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        graph_frame.grid_rowconfigure(0, weight=1)
        graph_frame.grid_columnconfigure(0, weight=1)
        self.start_date = DateEntry(
            self.master,
            width=12,
            background="darkblue",
            foreground="white",
            borderwidth=2,
        )
        self.start_date.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.master, text="End Date:").grid(row=0, column=2, padx=5, pady=5)
        self.end_date = DateEntry(
            self.master,
            width=12,
            background="darkblue",
            foreground="white",
            borderwidth=2,
        )
        self.end_date.grid(row=0, column=3, padx=5, pady=5)

        self.inflation_var = tk.BooleanVar()
        self.log_scale_var = tk.BooleanVar()
        ttk.Checkbutton(
            self.master,
            text="Inflation Adjusted",
            variable=self.inflation_var,
            command=self.update_graph,
        ).grid(row=8, column=0, columnspan=2, pady=5)
        ttk.Checkbutton(
            self.master,
            text="Logarithmic Scale",
            variable=self.log_scale_var,
            command=self.update_graph,
        ).grid(row=8, column=2, columnspan=2, pady=5)

        ttk.Label(self.master, text="Stock Tickers (comma-separated):").grid(
            row=1, column=0, columnspan=2, padx=5, pady=5
        )
        self.stock_entry = ttk.Entry(self.master, width=30)
        self.stock_entry.grid(row=1, column=2, columnspan=2, padx=5, pady=5)

        self.theme_var = tk.StringVar(value="dark")
        self.theme_switch = ttk.Checkbutton(
            self.master,
            text="Dark Mode",
            style="Switch.TCheckbutton",
            variable=self.theme_var,
            onvalue="dark",
            offvalue="light",
            command=self.toggle_theme,
        )
        self.theme_switch.grid(row=8, column=0, columnspan=4, pady=10)

        self.allocation_type = tk.StringVar(value="percentage")
        ttk.Radiobutton(
            self.master,
            text="Percentage",
            variable=self.allocation_type,
            value="percentage",
        ).grid(row=2, column=0, padx=5, pady=5)
        ttk.Radiobutton(
            self.master,
            text="Dollar Amount",
            variable=self.allocation_type,
            value="dollar",
        ).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.master, text="Allocations:").grid(
            row=3, column=0, padx=5, pady=5
        )
        self.allocation_entry = ttk.Entry(self.master, width=30)
        self.allocation_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

        ttk.Label(self.master, text="Baseline Stock:").grid(
            row=4, column=0, padx=5, pady=5
        )
        self.baseline_entry = ttk.Entry(self.master, width=10)
        self.baseline_entry.grid(row=4, column=1, padx=5, pady=5)

        button_frame = ttk.Frame(self.master)
        button_frame.grid(row=5, column=0, columnspan=4, pady=5)

        ttk.Button(
            button_frame, text="Save Configuration", command=self.save_backtest_config
        ).grid(row=0, column=0, padx=5)
        ttk.Button(
            button_frame, text="Load Configuration", command=self.load_backtest_config
        ).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Run Backtest", command=self.run_backtest).grid(
            row=0, column=2, padx=5
        )

        graph_frame = ttk.Frame(self.master)
        graph_frame.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        graph_frame.grid_rowconfigure(0, weight=1)
        graph_frame.grid_columnconfigure(0, weight=1)

        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=6, column=0, columnspan=4, padx=10, pady=10)
        self.canvas.callbacks.connect("resize_event", self.on_resize)
        self.results_text = tk.Text(self.master, height=5, width=80)
        self.results_text.grid(row=7, column=0, columnspan=4, padx=10, pady=10)

    def save_backtest_config(self):
        try:
            config = {
                "stocks": self.stock_entry.get(),
                "allocations": self.allocation_entry.get(),
                "allocation_type": self.allocation_type.get(),
                "baseline": self.baseline_entry.get(),
                "start_date": self.start_date.get_date().strftime("%Y-%m-%d"),
                "end_date": self.end_date.get_date().strftime("%Y-%m-%d"),
            }

            with open("backtest_config.txt", "w") as file:
                for key, value in config.items():
                    file.write(f"{key}:{value}\n")

            messagebox.showinfo("Success", "Configuration saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")

    def load_backtest_config(self):
        try:
            config = {}
            with open("backtest_config.txt", "r") as file:
                for line in file:
                    key, value = line.strip().split(":", 1)
                    config[key] = value

            self.stock_entry.delete(0, tk.END)
            self.stock_entry.insert(0, config.get("stocks", ""))
            self.allocation_entry.delete(0, tk.END)
            self.allocation_entry.insert(0, config.get("allocations", ""))
            self.allocation_type.set(config.get("allocation_type", "percentage"))
            self.baseline_entry.delete(0, tk.END)
            self.baseline_entry.insert(0, config.get("baseline", ""))

            if "start_date" in config:
                start_date = datetime.strptime(config["start_date"], "%Y-%m-%d").date()
                self.start_date.set_date(start_date)

            if "end_date" in config:
                end_date = datetime.strptime(config["end_date"], "%Y-%m-%d").date()
                self.end_date.set_date(end_date)

            messagebox.showinfo("Success", "Configuration loaded successfully!")
        except FileNotFoundError:
            messagebox.showwarning("Warning", "No saved configuration found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration: {str(e)}")

    def run_backtest(self):
        try:
            weights = []
            start_date = self.start_date.get_date()
            end_date = self.end_date.get_date()
            stocks = [s.strip() for s in self.stock_entry.get().split(",")]
            baseline_stock = self.baseline_entry.get().strip()
            allocation_type = self.allocation_type.get()
            allocations = [
                float(a.strip()) for a in self.allocation_entry.get().split(",")
            ]

            portfolio_data = yf.download(
                stocks + [baseline_stock],
                start=start_date,
                end=end_date,
                auto_adjust=False,
            )
            if portfolio_data.empty:
                messagebox.showerror(
                    "Error", "No data available for the selected stocks and date range"
                )
                return

            if len(stocks) != len(allocations):
                messagebox.showerror(
                    "Error", "Number of stocks must match number of allocations"
                )
                return

            close_data = portfolio_data["Close"]
            adj_close_data = portfolio_data["Adj Close"]

            if allocation_type == "percentage":
                if sum(allocations) != 100:
                    messagebox.showerror(
                        "Error", "Percentage allocations must sum to 100%"
                    )
                    return
                weights = [a / 100 for a in allocations]
                portfolio_value = pd.Series(0, index=close_data.index)
                for stock, weight in zip(stocks, weights):
                    portfolio_value += close_data[stock] * weight
            else:
                total_investment = sum(allocations)
                weights = [a / total_investment for a in allocations]
                portfolio_value = pd.Series(0, index=close_data.index)
                for stock, allocation in zip(stocks, allocations):
                    shares = allocation / close_data[stock].iloc[0]
                    portfolio_value += close_data[stock] * shares

            portfolio_return = (
                sum(
                    (adj_close_data[stock].iloc[-1] / adj_close_data[stock].iloc[0] - 1)
                    * weight
                    for stock, weight in zip(stocks, weights)
                )
                * 100
            )
            baseline_return = (
                adj_close_data[baseline_stock].iloc[-1]
                / adj_close_data[baseline_stock].iloc[0]
                - 1
            ) * 100

            self.portfolio_data = portfolio_value / portfolio_value.iloc[0]
            self.baseline_data = (
                close_data[baseline_stock] / close_data[baseline_stock].iloc[0]
            )
            self.dates = portfolio_value.index

            self.update_graph()

            days = (end_date - start_date).days
            portfolio_annualized_return = (
                (portfolio_value.iloc[-1] / portfolio_value.iloc[0]) ** (365 / days) - 1
            ) * 100
            baseline_annualized_return = (
                (
                    adj_close_data[baseline_stock].iloc[-1]
                    / adj_close_data[baseline_stock].iloc[0]
                )
                ** (365 / days)
                - 1
            ) * 100

            self.results_text.delete("1.0", tk.END)
            self.results_text.insert(
                tk.END, f"Portfolio Return: {portfolio_return:.2f}%\n"
            )
            self.results_text.insert(
                tk.END,
                f"Portfolio Annualized Return: {portfolio_annualized_return:.2f}%\n",
            )
            self.results_text.insert(
                tk.END, f"Baseline Return ({baseline_stock}): {baseline_return:.2f}%\n"
            )
            self.results_text.insert(
                tk.END,
                f"Baseline Annualized Return: {baseline_annualized_return:.2f}%\n",
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_resize(self, event):
        self.fig.set_size_inches(
            event.width / self.fig.dpi, event.height / self.fig.dpi
        )
        self.canvas.draw()

    def update_graph(self):
        self.ax.clear()

        portfolio_data = self.portfolio_data
        baseline_data = self.baseline_data

        if self.inflation_var.get():
            inflation_data = self.get_inflation_data()
            cumulative_inflation = (1 + inflation_data).cumprod()
            portfolio_data = portfolio_data / cumulative_inflation
            baseline_data = baseline_data / cumulative_inflation

        self.ax.plot(self.dates, portfolio_data, label="Portfolio")
        self.ax.plot(self.dates, baseline_data, label=self.baseline_entry.get().strip())

        self.ax.set_title("Portfolio Performance vs Baseline")
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Normalized Value")

        if self.log_scale_var.get():
            self.ax.set_yscale("log")
        else:
            self.ax.set_yscale("linear")

        self.ax.legend()
        self.canvas.draw()
        self.master.update_idletasks()

    def get_inflation_data(self) -> int:
        country = "united-states"  # You can make this configurable
        raw_data = self.get_inflation_data(country)
        processed_data = self.process_inflation_data(raw_data)

        # Resample to match your stock data frequency and fill missing values
        resampled_data = processed_data.resample("D").ffill()

        # Align with your stock data date range
        aligned_data = resampled_data.loc[self.dates[0] : self.dates[-1]]

        return aligned_data

    def process_inflation_data(inflation_data):
        if not inflation_data:
            return pd.Series()

        df = pd.DataFrame(inflation_data)
        df["Date"] = pd.to_datetime(df["Date"])
        df.set_index("Date", inplace=True)
        df["InflationRate"] = df["InflationRate"] / 100  # Convert to decimal
        return df["InflationRate"].sort_index()

    def get_inflation_data(country="united-states"):
        url = f"https://www.statbureau.org/get-data-json?country={country}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching inflation data: {e}")
            return None
