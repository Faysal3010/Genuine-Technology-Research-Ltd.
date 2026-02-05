import yfinance as yf

class TradingStrategy:
    def __init__(self, symbol, start_date, end_date, budget=5000):
        """
        :param symbol: company symbol
        :param start_date: date to start
        :param end_date: date to end
        :param budget: budget to invest
        """
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.budget = budget
        self.data = None
        self.position = 0
        self.buy_price = 0
        self.shares = 0
        self.profit = 0

    def get_data_clean_up(self):
        """download data from yahoo finance, clean up the data and save it to csv"""
        # download data
        self.data = yf.download(self.symbol, start=self.start_date, end=self.end_date)
        # Store only first header and remove all header
        self.data.columns = self.data.columns.get_level_values(0)
        # remove duplicate
        self.data = self.data[~self.data.index.duplicated(keep='first')]
        # fill up NaN fill
        self.data.ffill(inplace=True)
        # optional to visualize the data in csv formate
        self.data.to_csv("data.csv")

    def add_indicators_50_200(self):
           """Compute the moving averages for 50 and 200 days."""
           self.data["MA50"] = self.data["Close"].rolling(50).mean()
           self.data["MA200"] = self.data["Close"].rolling(200).mean()


    def run_strategy(self):
        """:Golden Opportunity: Identify the golden cross, signaling a bullish trend, and take a buying position. 
        :Investment Strategy: Determine the maximum quantity of shares to purchase within the $5000 budget. 
        :Timely Actions: When the golden cross reverses, sell the position and close the trade. When you are in a position you can’t buy other stock.
        :Final Touches: Forcefully close the position on the last row if a position is still open."""
        for i in range(len(self.data)):
            row = self.data.iloc[i]

            # Golden Cross Buy
            if row['MA50'] > row['MA200'] and self.position == 0:
                self.buy_price = row['Close']
                self.shares = int(self.budget // self.buy_price)
                self.position = 1
                print(f"BUY {self.shares} shares at {self.buy_price} on {self.data.index[i]}")

            # Death Cross Sell
            elif row['MA50'] < row['MA200'] and self.position == 1:
                sell_price = row['Close']
                self.profit += (sell_price - self.buy_price) * self.shares
                self.position = 0
                print(f"SELL {self.shares} shares at {sell_price} on {self.data.index[i]}")

        # Ending Day Force Sell
        if self.position == 1:
            sell_price = self.data.iloc[-1]['Close']
            self.profit += (sell_price - self.buy_price) * self.shares
            print(f"FORCE SELL {self.shares} shares at {sell_price} on {self.data.index[-1]}")
            self.position = 0

    def evaluate(self):
        """:Evaluation: Calculate profits or losses to assess the success of the trading strategy."""
        if self.profit >= 0:
            print(f"Net Profit: ${self.profit:.2f}")
        else:
            print(f"Net Loss: ${abs(self.profit):.2f}")


