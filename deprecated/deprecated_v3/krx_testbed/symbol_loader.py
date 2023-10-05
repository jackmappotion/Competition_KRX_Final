class SYMBOL_LOADER:
    @staticmethod
    def load_symbols_df():
        symbols_df = kq.symbol_stock()
        return symbols_df

    class SYMBOL_FILTER:
        @staticmethod
        def filter__market(symbols_df):
            filtered_symbols_df = symbols_df[
                (symbols_df["MARKET"].isin(["코스닥", "유가증권"]))
            ].copy()
            return filtered_symbols_df

        @staticmethod
        def filter__admin_issue(symbols_df):
            filtered_symbols_df = symbols_df[(symbols_df["ADMIN_ISSUE"] == 0)].copy()
            return filtered_symbols_df

        @staticmethod
        def filter_sec_type(symbols_df):
            filtered_symbols_df = symbols_df[
                symbols_df["SEC_TYPE"].isin(["ST", "EF", "EN"])
            ].copy()
            return filtered_symbols_df

    def filter_symbols_df(self, symbols_df):
        symbol_filter = self.SYMBOL_FILTER()
        filtered_symbols_df = symbol_filter.filter__market(symbols_df)
        filtered_symbols_df = symbol_filter.filter__admin_issue(filtered_symbols_df)
        filtered_symbols_df = symbol_filter.filter_sec_type(filtered_symbols_df)
        return filtered_symbols_df

    @staticmethod
    def get_symbols(symbols_df):
        symbols = sorted(set(symbols_df["SYMBOL"]))
        return symbols

    # SYMBOL_LOADER PIPELINE
    def __call__(self):
        symbols_df = self.load_symbols_df()
        filtered_symbols_df = self.filter_symbols_df(symbols_df)
        symbols = self.get_symbols(filtered_symbols_df)
        return symbols