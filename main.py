import tkinter as tk
from stock_backtest_app import StockBacktestApp

if __name__ == "__main__":
    root = tk.Tk()
    app = StockBacktestApp(root)

    # Configure the main window to be resizable
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.update_idletasks()

    # Make sure window is resizable
    root.resizable(True, True)

    # Set minimum window size
    root.minsize(800, 600)

    root.mainloop()
