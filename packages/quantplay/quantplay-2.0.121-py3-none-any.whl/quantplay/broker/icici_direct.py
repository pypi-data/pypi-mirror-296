from datetime import datetime, date
from typing import Any, Literal
from breeze_connect.breeze_connect import BreezeConnect  # type: ignore

from quantplay.broker.generics.broker import Broker

# from quantplay.model.broker import (
#     MarginsResponse,
#     ModifyOrderRequest,
#     UserBrokerProfileResponse,
# )

# Initialize SDK

api_key = "T1233357*547X^F9Ij052116M59Gb981"
api_secret = "5374^R9I82259698182rm5701#9N699$"
session_token = "47120472"

interval = "1second"
stock_code = "NIFTY"
exch_code = "NFO"
from_date = "2022-10-10T00:00:00.000Z"
to_date = "2022-11-11T00:00:00.000Z"
product_type = "Options"
expiry_date = "2022-11-24T00:00:00.000Z"
right = "Call"
strike_price = "18000"


class ICICI(Broker):
    index_map = {"FINNIFTY": "NIFFIN", "BANKNIFTY": "CNXBAN", "MIDCPNIFTY": "NIFSEL"}

    def __init__(
        self,
        api_key: str | None = None,
        api_secret: str | None = None,
        session_token: str | None = None,
    ) -> None:
        if api_key and api_secret and session_token:
            self.wrapper = BreezeConnect(api_key)
            self.wrapper.generate_session(api_secret, session_token)  # type: ignore

    def get_historical_data(
        self,
        interval: Literal["1second", "1minute", "5minute", "30minute", "1day"],
        from_date: datetime,
        to_date: datetime,
        stock_code: str,
        exch_code: Literal["NSE", "NFO", "BSE", "NDX", "MCX"],
        product_type: Literal["Cash", "Options", "Futures"] | None,
        expiry_date: date | None,
        right: Literal["Call", "Put", "Others"] | None,
        strike_price: int | None,
    ):
        from_date_str = from_date.isoformat()[:19] + ".000Z"
        to_date_str = to_date.isoformat()[:19] + ".000Z"

        expiry_date_str = expiry_date.isoformat()[:19] + ".000Z" if expiry_date else ""

        data: Any = self.wrapper.get_historical_data_v2(
            interval,
            from_date_str,
            to_date_str,
            stock_code,
            exch_code,
            product_type,  # type: ignore
            expiry_date_str,
            right,  # type: ignore
            str(strike_price),
        )

        print(data)

    # def orders(self, tag: str | None = None, add_ltp: bool = True) -> DataFrame:
    #     return super().orders(tag, add_ltp)

    # def positions(self, drop_cnc: bool = True) -> DataFrame:
    #     return super().positions(drop_cnc)

    # def place_order(
    #     self,
    #     tradingsymbol: str,
    #     exchange: Literal["NSE"]
    #     | Literal["BSE"]
    #     | Literal["NFO"]
    #     | Literal["BFO"]
    #     | Literal["CDS"]
    #     | Literal["BCD"]
    #     | Literal["MCX"],
    #     quantity: int,
    #     order_type: Literal["MARKET"]
    #     | Literal["LIMIT"]
    #     | Literal["SL"]
    #     | Literal["SL-M"],
    #     transaction_type: Literal["SELL"] | Literal["BUY"],
    #     tag: str | None,
    #     product: Literal["NRML"] | Literal["MIS"] | Literal["CNC"],
    #     price: float,
    #     trigger_price: float | None = None,
    # ) -> str | None:
    #     return super().place_order(
    #         tradingsymbol,
    #         exchange,
    #         quantity,
    #         order_type,
    #         transaction_type,
    #         tag,
    #         product,
    #         price,
    #         trigger_price,
    #     )

    # def modify_order(self, order: ModifyOrderRequest) -> str:
    #     return super().modify_order(order)

    # def cancel_order(self, order_id: str, variety: str | None = None) -> None:
    #     return super().cancel_order(order_id, variety)

    # def holdings(self) -> DataFrame:
    #     return super().holdings()

    # def margins(self) -> MarginsResponse:
    #     return super().margins()

    # def ltp(
    #     self,
    #     exchange: Literal["NSE"]
    #     | Literal["BSE"]
    #     | Literal["NFO"]
    #     | Literal["BFO"]
    #     | Literal["CDS"]
    #     | Literal["BCD"]
    #     | Literal["MCX"],
    #     tradingsymbol: str,
    # ) -> float:
    #     return super().ltp(exchange, tradingsymbol)

    # def profile(self) -> UserBrokerProfileResponse:
    #     return super().profile()

    # def get_exchange(
    #     self,
    #     exchange: Literal["NSE"]
    #     | Literal["BSE"]
    #     | Literal["NFO"]
    #     | Literal["BFO"]
    #     | Literal["CDS"]
    #     | Literal["BCD"]
    #     | Literal["MCX"],
    # ) -> ...:
    #     return super().get_exchange(exchange)

    # def get_product(
    #     self, product: Literal["NRML"] | Literal["MIS"] | Literal["CNC"]
    # ) -> ...:
    #     return super().get_product(product)

    # def get_order_type(
    #     self,
    #     order_type: Literal["MARKET"]
    #     | Literal["LIMIT"]
    #     | Literal["SL"]
    #     | Literal["SL-M"],
    # ) -> ...:
    #     return super().get_order_type(order_type)
