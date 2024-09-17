from collections.abc import Callable
from datetime import datetime, date
from typing import Any, Literal
from breeze_connect.breeze_connect import BreezeConnect  # type: ignore

from quantplay.broker.generics.broker import Broker
import polars as pl

from quantplay.model.broker import (
    MarginsResponse,
    ModifyOrderRequest,
    UserBrokerProfileResponse,
)
from quantplay.model.generics import (
    ExchangeType,
    OrderTypeType,
    ProductType,
    TransactionType,
)

api_key = "2721)7972f2cxz733k4NGt933$23h17D"
api_secret = "4e620^i919469f7~1709*066#d384&5y"
session_token = "47204416"


class RateLimitExcededException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class NoDataException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ICICI(Broker):
    index_map = {
        "FINNIFTY": "NIFFIN",
        "BANKNIFTY": "CNXBAN",
        "MIDCPNIFTY": "NIFSEL",
    }

    def __init__(
        self,
        api_key: str | None = None,
        api_secret: str | None = None,
        session_token: str | None = None,
        load_instrument: bool = False,
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
    ) -> pl.DataFrame:
        from_date_str = from_date.isoformat()[:19] + ".000Z"
        to_date_str = to_date.isoformat()[:19] + ".000Z"

        expiry_date_str = expiry_date.isoformat()[:19] + ".000Z" if expiry_date else ""

        historical_fetch_fn = (
            self.wrapper.get_historical_data_v2
            if interval == "1second"
            else self.wrapper.get_historical_data
        )

        data = self.invoke_wrapper(
            historical_fetch_fn,
            interval=interval,
            from_date=from_date_str,
            to_date=to_date_str,
            stock_code=stock_code,
            exchange_code=exch_code,
            product_type=product_type,
            expiry_date=expiry_date_str,
            right=right,
            strike_price=str(strike_price),
        )

        print(data)

        if data["Success"] is None or len(data["Success"]) == 0:
            raise NoDataException(f"Historical Data For {data}")

        return pl.from_dicts(data["Success"])

    def orders(self, tag: str | None = None, add_ltp: bool = True) -> pl.DataFrame:
        return pl.DataFrame(schema=self.orders_schema)

        orders = self.invoke_wrapper(self.wrapper.get_order_list, exchange_code="NFO")

        if orders is None:
            return pl.DataFrame(schema=self.orders_schema)

    def positions(self, drop_cnc: bool = True) -> pl.DataFrame:
        return pl.DataFrame(schema=self.positions_schema)

        positions = self.invoke_wrapper(self.wrapper.get_portfolio_positions)

        if positions is None:
            return pl.DataFrame(schema=self.positions_schema)

    def place_order(
        self,
        tradingsymbol: str,
        exchange: ExchangeType,
        quantity: int,
        order_type: OrderTypeType,
        transaction_type: TransactionType,
        tag: str | None,
        product: ProductType,
        price: float,
        trigger_price: float | None = None,
    ) -> str | None:
        return

    def modify_order(self, order: ModifyOrderRequest) -> str:
        return ""

    def cancel_order(self, order_id: str, variety: str | None = None) -> None:
        return

    def holdings(self) -> pl.DataFrame:
        return pl.DataFrame(schema=self.holidings_schema)

    def margins(self) -> MarginsResponse:
        margins = self.invoke_wrapper(self.wrapper.get_funds)

        return {
            "total_balance": margins["total_bank_balance"],
            "margin_available": (
                margins["allocated_equity"]
                + margins["allocated_fno"]
                + margins["allocated_commodity"]
                + margins["allocated_currency"]
            ),
            "margin_used": (
                margins["block_by_trade_equity"]
                + margins["block_by_trade_fno"]
                + margins["block_by_trade_commodity"]
                + margins["block_by_trade_currency"]
            ),
            "cash": margins["unallocated_balance"],
        }

    def ltp(self, exchange: ExchangeType, tradingsymbol: str) -> float:
        return 0.0

    def profile(self) -> UserBrokerProfileResponse:
        return {
            "user_id": "",
        }

    def get_exchange(self, exchange: ExchangeType) -> ...:
        return

    def get_product(self, product: ProductType) -> ...:
        return

    def get_order_type(self, order_type: OrderTypeType) -> ...:
        return

    def get_icici_symbol_param(self):
        pass

    def invoke_wrapper(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        try:
            data = fn(*args, **kwargs)

            print(data)

            if data["Status"] > 200:
                if data["Error"] == "Limit exceed: API call per day: ":
                    raise RateLimitExcededException(data["Error"])

                raise Exception(data["Error"])

            return data["Success"]

        except Exception as e:
            raise (e)
