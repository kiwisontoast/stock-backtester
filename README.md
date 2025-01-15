# Stock-Backtesting
StockBacktesting enables users to perform historical analysis and backtesting of stock portfolios. This interactive tool allows users to visualize and compare portfolio performance against benchmark stocks

## Key Features 
### Portfolio Analysis 
- Portfolio construction with multi-stock comparison 
- Both percentage-based and fixed-dollar allocations 
- Historical performance comparison against benchmark stocks 
- Logarithmic and linear scale visualization options 
- Real-time data fetching via yfinance API 
### Visualization 
- Dynamic graph resizing 
- Dark/Light theme toggle 
- Interactive performance charts 
- Customizable date ranges 
### Data Management 
- Save and load portfolio configurations 
- Export functionality for analysis results 
- Detailed performance metrics including: 
    - Total portfolio return 
    - Annualized returns 
    - Baseline return 
    - Baseline annualized return 
### User Interface 
- Clean, modern interface using ttk styling 
- Real-time graph updates 
- Error handling and user feedback 
- Responsive design that adapts to window resizing 
- Intuitive date selection using a calendar

 ## Dependencies
 - This project requires: 
 ~ tkinter 
 ~ pandas 
 ~ yfinance 
 ~ sv_ttk 
 ~ datetime 
 ~ tkcalendar 
 ~ matplotlib 

 ## Usage 
 ### Basic Operation 
 - Launch the Application 
 - Enter stock tickers (comma-seperated) 
 - Specify your allocations in either percentage or dollar amounts 
 - Select a date-range for analysis 
 - Choose a benchmark stock for comparison 
 - Click "Run Backtest" to generate results 
 ### Configuration Management 
 - Save configurations for future use with "Save Configuration" 
 - Load previously saved setups using "Load Configuration" 
 - Adjust visualization preferences (logarithmic scale) 
 ### Visualization Options 
 - Toggle between dark and light themes 
 - Switch between linear and logarithmic scales 
 - Interact with dynamic charts 

 ## Warnings 
 ### Data Retrieval 
 - Ensure valid stock tickers are entered 
 - Verify allocation percentages sum to 100% when using percentage mode 
 -Check that allocation amounts are reasonable in dollar mode 
 - Some stocks may have limited historical data availability 
 ### Performance - Processing time increases with the number of stocks and longer date ranges 
 - Large datasets may take longer to fetch and display 
 ### Files 
 - Configuration files may be overwritten when saving new setups 
 
 ## Authors 
 Dev Shroff & Krishnika Anandan