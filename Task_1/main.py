from trend import TradingStrategy

strategy = TradingStrategy("AAPL", "2018-01-01", "2023-12-31", budget=5000)
strategy.get_data_clean_up()
strategy.add_indicators_50_200()
strategy.run_strategy()
strategy.evaluate()
