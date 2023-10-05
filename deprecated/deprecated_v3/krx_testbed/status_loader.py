class STATUS_LOADER:
    def __init__(self, dict_df_result, dict_df_position) -> None:
        self.dict_df_result = dict_df_result
        self.dict_df_position = dict_df_position

    def get_current_cash(self):
        _dict_df_result = self.dict_df_result
        try:
            _df_result_total = _dict_df_result["TOTAL"]
            _current_cash = (
                _df_result_total.sort_values("DATE").tail(1)["CASH"].values[0]
            )
            return _current_cash
        except:
            return 1_000_000_000

    def get_current_symbol_df(self):
        current_symbol_list = list()
        _dict_df_result = self.dict_df_result
        _dict_df_position = self.dict_df_position
        
        _total_symbols = sorted(_dict_df_position.keys())

        for _symbol in _total_symbols:
            try:
                _symbol_result_df = _dict_df_result[_symbol]
                _symbol_position_df = _dict_df_position[_symbol]

                _current_price = (
                    _symbol_result_df.sort_values("DATE").tail(1)["PRICE"].values[0]
                )
                _trade_price = _symbol_position_df["TRADE_PRICE"].values[0]
                _current_qty = _symbol_position_df["QTY"].values[0]

                current_symbol_list.append(
                    {
                        "symbol": _symbol,
                        "current_qty": _current_qty,
                        "current_price": _current_price,
                        "trade_price": _trade_price,
                    }
                )
            except:
                pass
        return pd.DataFrame(current_symbol_list)