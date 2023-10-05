""" 
symbols_and_orders
"""


from typing import Any


class FUDAMENTAL_PROCESSOR:
    def __init__(self, fundamental_df) -> None:
        fundamental_df["pbr"] = fundamental_df["marketcap"] / (
            fundamental_df["capital"] * 1000
        )
        self.fundamental_df = fundamental_df

    class GET_BUYING_ORDERS:
        def __init__(self, fundamental_processor, daily_invest_money) -> None:
            self.fundamental_processor = fundamental_processor
            self.daily_invest_money = daily_invest_money

        @staticmethod
        def get_low_pbr_df(fundamental_df):
            low_pbr_df = fundamental_df.nsmallest(5, "pbr")
            return low_pbr_df

        @staticmethod
        def append_pbr_weight(low_pbr_df):
            low_pbr_df["pbr_weight"] = low_pbr_df["pbr"].sum() / low_pbr_df["pbr"]
            return low_pbr_df

        @staticmethod
        def append_price_invest(low_pbr_df, daily_invest_money):
            low_pbr_df["price_invest"] = (
                low_pbr_df["pbr_weight"] / low_pbr_df["pbr_weight"].sum()
            ) * daily_invest_money

        @staticmethod
        def append_cnt_invest(low_pbr_df):
            low_pbr_df["cnt_invest"] = low_pbr_df["price_invest"] // low_pbr_df["close"]
            return low_pbr_df

        def __call__(self, daily_invest_money):
            fundamental_df = self.fundamental_processor.fundamental_df
            daily_invest_money = self.daily_invest_money
            low_pbr_df = self.get_low_pbr_df(fundamental_df)
            low_pbr_df = self.append_pbr_weight(fundamental_df)
            low_pbr_df = self.append_price_invest(fundamental_df, daily_invest_money)
            low_pbr_df = self.append_cnt_invest(fundamental_df)
            buying_orders = list(
                low_pbr_df.set_index("symbol")["cnt_invest"]
                .astype(int)
                .to_dict()
                .items()
            )
            return buying_orders

    class GET_SELLING_ORDERS:
        def __init__(self, fundamental_processor, status_df) -> None:
            self.fundamental_processor = fundamental_processor
            self.status_df = status_df

        @staticmethod
        def get_limit_line(fundamental_df):
            # limit_line : PBR 상위 75 %
            limit_line = np.percentile(fundamental_df["PBR"], 75)
            return limit_line

        @staticmethod
        def get_high_pbr_df(fundamental_df, limit_line):
            high_pbr_df = fundamental_df[fundamental_df["PBR"] > limit_line]
            return high_pbr_df

        @staticmethod
        def filter_position_symbols(high_pbr_df, position_symbols):
            filtered_position_symbols = sorted(
                set(high_pbr_df["SYMBOL"]) & set(position_symbols)
            )
            return filtered_position_symbols

        def __call__(self):
            fundamental_df = self.fundamental_processor.fundamental_df
            status_df = self.status_df
            position_symbols = sorted(set(status_df["SYMBOL"]))

            limit_line = self.get_limit_line(fundamental_df)
            high_pbr_df = self.get_high_pbr_df(fundamental_df, limit_line)
            filtered_position_symbols = self.filter_position_symbols(
                high_pbr_df, position_symbols
            )
            selling_df = status_df[status_df["SYMBOL"].isin(filtered_position_symbols)]

            selling_orders = list(
                selling_df.set_index("symbol")["current_qty"]
                .apply(lambda x: x * -1)
                .astype(int)
                .to_dict()
                .items()
            )
            return selling_orders