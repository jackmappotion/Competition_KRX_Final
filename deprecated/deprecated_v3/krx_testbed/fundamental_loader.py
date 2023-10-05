class FUNDAMENTAL_LOADER:
    def __init__(self, symbol, date) -> None:
        self.symbol = symbol
        self.date = date
        self.daily_stock_df = kq.daily_stock(
            symbol,
            start_date=date - dt.timedelta(days=7),
            end_date=date,
        )

    def load_recent_close(self):
        daily_stock_df = self.daily_stock_df
        _close = daily_stock_df.sort_values("DATE").tail(1)["CLOSE"].values[0]
        return _close

    def load_recent_marketcap(self):
        daily_stock_df = self.daily_stock_df
        _marketcap = daily_stock_df.sort_values("DATE").tail(1)["MARKETCAP"].values[0]
        return _marketcap

    def load_recent_netprofit(self):
        netprofit_df = kq.account_history(self.symbol, "122700")
        netprofit_df.sort_values("YEARMONTH", inplace=True)
        _netprofit = netprofit_df.tail(1)["VALUE"].values[0]
        return _netprofit

    def load_recent_capital(self):
        capital_df = kq.account_history(self.symbol, "115000")
        capital_df.sort_values("YEARMONTH", inplace=True)
        _capital = capital_df.tail(1)["VALUE"].values[0]
        return _capital

    def __call__(self):
        _close = self.load_recent_close()
        _marketcap = self.load_recent_marketcap()
        _netprofit = self.load_recent_netprofit()
        _capital = self.load_recent_capital()
        return {
            "symbol": self.symbol,
            "close": _close,
            "marketcap": _marketcap,
            "netprofit": _netprofit,
            "capital": _capital,
        }
