from collections.abc import Callable
from datetime import datetime, date, timedelta
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
from quantplay.utils.constant import Constants
from quantplay.utils.pickle_utils import InstrumentData
from quantplay.wrapper.aws.s3 import S3Utils

api_key = "2721)7972f2cxz733k4NGt933$23h17D"
api_secret = "4e620^i919469f7~1709*066#d384&5y"
session_token = "47204416"


class RateLimitExcededException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class NoDataException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


logger = Constants.logger


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
        load_instrument: bool = True,
    ) -> None:
        if api_key and api_secret and session_token:
            self.wrapper = BreezeConnect(api_key) # type:ignore
            self.wrapper.generate_session(api_secret, session_token)  # type: ignore

        if load_instrument:
            self.load_instrument()

    def load_instrument(self, file_name: str | None = None) -> None:
        try:
            self.symbol_data = InstrumentData.get_instance().load_data(  # type: ignore
                "icici_instruments"
            )
            Constants.logger.info("[LOADING_INSTRUMENTS] loading data from cache")
        except Exception:
            inst_data_df = S3Utils.get_parquet(
                "quantplay-market-data/symbol_data/icici_instruments.parquet"
            )
            self.instrument_data = inst_data_df
            self.initialize_symbol_data_v2(save_as="icici_instruments")

        self.initialize_broker_symbol_map()

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

    def get_symbol(self, symbol: str, exchange: ExchangeType | None = None):
        if symbol not in self.quantplay_symbol_map:
            return symbol

        return self.quantplay_symbol_map[symbol]

    def orders(self, tag: str | None = None, add_ltp: bool = True) -> pl.DataFrame:
        to_date = datetime.now().isoformat()[:19] + ".000Z"
        from_date = (datetime.now() - timedelta(hours=10)).isoformat()[:19] + ".000Z"

        orders = self.wrapper.get_order_list(
            exchange_code="NFO",
            from_date=from_date,
            to_date=to_date,
        )
        orders_df = pl.DataFrame(orders["Success"])
        orders_df = orders_df.rename(
            {
                "order_datetime": "order_timestamp",
                "action": "transaction_type",
                "exchange_code": "exchange",
                "expiry_date": "expiry",
                "strike_price": "strike",
            }
        )
        orders_df = orders_df.with_columns(
            pl.col("expiry").str.strptime(pl.Date, format="%d-%b-%Y").alias("expiry"),
            pl.col("order_timestamp")
            .str.strptime(pl.Datetime(time_unit="ms"), format="%d-%b-%Y %H:%M:%S")
            .alias("order_timestamp"),
            pl.col("order_type").str.to_uppercase().alias("order_type"),
            pl.col("transaction_type").str.to_uppercase().alias("transaction_type"),
            pl.col("status").str.to_uppercase().alias("status"),
            pl.when(pl.col("right") == "Call")
            .then(pl.lit("CE"))
            .when(pl.col("right") == "Put")
            .then(pl.lit("PE"))
            .alias("instrument_type"),
        )

        orders_df = orders_df.with_columns(
            (
                pl.col("stock_code")
                + "-"
                + pl.col("expiry").dt.date().cast(pl.String)
                + "-"
                + pl.col("strike").cast(pl.String)
                + "-"
                + pl.col("instrument_type").cast(pl.String)
            ).alias("tradingsymbol")
        )

        orders_df = orders_df.with_columns(
            pl.struct(["exchange", "tradingsymbol"])
            .map_elements(
                lambda x: int(
                    self.symbol_attribute(x["exchange"], x["tradingsymbol"], "token")
                ),
                return_dtype=pl.Int64,
            )
            .alias("token")
        )

        orders_df = orders_df.with_columns(
            pl.lit(None).alias("user_id"),
            pl.lit("NRML").alias("product"),
            pl.lit("regular").alias("variety"),
            pl.lit("default").alias("tag"),
            pl.lit(None).alias("trigger_price"),
            pl.lit(None).alias("ltp"),
            pl.lit(None).alias("filled_quantity"),
            pl.lit(None).alias("status_message"),
            pl.lit(None).alias("status_message_raw"),
            pl.col("order_timestamp").alias("update_timestamp"),
        )

        return orders_df[list(self.orders_schema.keys())].cast(self.orders_schema)

    def positions(self, drop_cnc: bool = True) -> pl.DataFrame:
        to_date = datetime.now().isoformat()[:19] + ".000Z"
        from_date = (datetime.now() - timedelta(hours=10)).isoformat()[:19] + ".000Z"
        positions = self.wrapper.get_portfolio_holdings(
            exchange_code="NFO",
            from_date=from_date,
            to_date=to_date,
            stock_code="",
            portfolio_type="",
        )
        positions_df = pl.DataFrame(positions["Success"])

        positions_df = positions_df.rename(
            {
                "exchange_code": "exchange",
                "expiry_date": "expiry",
                "strike_price": "strike",
                "product_type": "product",
            }
        )
        positions_df = positions_df.with_columns(
            pl.col("strike").cast(pl.Float32).alias("strike"),
            pl.col("expiry").str.strptime(pl.Date, format="%d-%b-%Y").alias("expiry"),
            pl.when(pl.col("right") == "Call")
            .then(pl.lit("CE"))
            .when(pl.col("right") == "Put")
            .then(pl.lit("PE"))
            .alias("instrument_type"),
        )

        positions_df = positions_df.with_columns(
            (
                pl.col("stock_code")
                + "-"
                + pl.col("expiry").dt.date().cast(pl.String)
                + "-"
                + pl.col("strike").cast(pl.String)
                + "-"
                + pl.col("instrument_type").cast(pl.String)
            ).alias("tradingsymbol")
        )

        positions_df = positions_df.with_columns(
            pl.struct(["exchange", "tradingsymbol"])
            .map_elements(
                lambda x: int(
                    self.symbol_attribute(x["exchange"], x["tradingsymbol"], "token")
                ),
                return_dtype=pl.Int64,
            )
            .alias("token")
        )

        positions_df = positions_df.with_columns(
            pl.lit(0).alias("sell_value"),
            pl.lit(0).alias("buy_value"),
            pl.lit(0).alias("ltp"),
            pl.lit(0).alias("sell_quantity"),
            pl.lit("NRML").alias("product"),
            pl.lit(0).alias("buy_quantity"),
            pl.col("instrument_type").alias("option_type"),
            (
                pl.col("unrealized_profit").cast(pl.Float32)
                + pl.col("realized_profit").cast(pl.Float32)
            ).alias("pnl"),
        )
        return positions_df[list(self.positions_schema.keys())].cast(
            self.positions_schema
        )

    def get_right(self, symbol_data):
        if symbol_data["instrument_type"] == "CE":
            return "call"
        elif symbol_data["instrument_type"] == "PE":
            return "put"

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
        icici_tradingsymbol = self.get_symbol(tradingsymbol)
        symbol_data = self.symbol_data[f"{exchange}:{icici_tradingsymbol}"]
        icici_product = "cash"
        if exchange in ["NFO", "BFO"]:
            icici_product = "futures"
            if tradingsymbol[-2:] in ["PE", "CE"]:
                icici_product = "options"
        if icici_product == "cash":
            self.wrapper.place_order(
                stock_code=icici_tradingsymbol,
                exchange_code=exchange,
                product="cash",
                action=transaction_type.lower(),
                order_type=order_type.lower(),
                stoploss="",
                quantity=str(quantity),
                price=str(price),
                validity="day",
            )
        else:
            response = self.wrapper.place_order(
                stock_code=symbol_data["symbol_code"],
                exchange_code="NFO",
                product=icici_product,
                action=transaction_type.lower(),
                order_type=order_type.lower(),
                stoploss="",
                quantity=str(quantity),
                price=str(price),
                validity="day",
                expiry_date=str(symbol_data["expiry"]) + "T06:00:00.000Z",
                right=self.get_right(symbol_data),
                strike_price=str(symbol_data["strike"]),
            )
        return response["Success"]["order_id"]

    def modify_order(self, order: ModifyOrderRequest) -> str:
        return ""

    def cancel_order(self, order_id: str, variety: str | None = None) -> None:
        orders = self.orders()
        order = orders.filter(pl.col("order_id") == order_id)
        if len(order) == 0:
            return
        order_details = order.to_dicts()[0]
        self.wrapper.cancel_order(  # type:ignore
            exchange_code=order_details["exchange"], order_id=order_id
        )
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
                + margins["unallocated_balance"]
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
