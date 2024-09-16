import asyncio
from datetime import datetime, timedelta
from typing import Type

import numpy as np
from ccxt.async_support.base.ws.order_book import OrderBook as _Orderbook
from loguru import logger
from sqlalchemy.orm import Session

from plutous import database as db
from plutous.enums import Exchange
from plutous.trade.crypto.enums import CollectorType
from plutous.trade.crypto.models import BidAskSum, Orderbook

from .base import BaseCollector

TIMEOUT = timedelta(minutes=5)


class OrderbookCollector(BaseCollector):
    COLLECTOR_TYPE = CollectorType.ORDERBOOK
    TABLE: Type[Orderbook] = Orderbook

    def __init__(
        self,
        exchange: Exchange,
        symbols: list[str] | None = None,
        rate_limit: bool = False,
    ):
        super().__init__(exchange, symbols, rate_limit)
        self.exchange.options["watchOrderBookLimit"] = 5000  # type: ignore

    async def collect(self):
        active_symbols = await self.fetch_active_symbols()
        await self.exchange.watch_order_book_for_symbols(active_symbols)
        await asyncio.sleep(1)

        if self.exchange.orderbooks is None:
            raise RuntimeError("No orderbooks found")

        # Fetch the last snapshot of the orderbook and update miss prices
        with db.Session() as session:
            orderbook_snapshot = self.fetch_orderbook_snapshot(active_symbols, session)

        logger.info(
            f"Orderbook snapshot fetched for symbols: {orderbook_snapshot.keys()}"
        )

        for symbol, snapshot in orderbook_snapshot.items():
            for side in ["bids", "asks"]:
                for price, volume in self.exchange.orderbooks[symbol][side]:
                    snapshot[side].store(price, volume)
                self.exchange.orderbooks[symbol][side] = snapshot[side]

        while True:
            ob_data = []
            bas_data = []
            if set(self.exchange.orderbooks.keys()) != set(active_symbols):
                logger.error(
                    f"Active symbols: {active_symbols}, Orderbook symbols: {self.exchange.orderbooks.keys()}"
                )
                raise RuntimeError("Active symbols do not match orderbook symbols")

            for symbol, orderbook in self.exchange.orderbooks.items():
                logger.info(f"Processing orderbook for {symbol}")

                while (lastest_bid := orderbook["bids"][0][0]) > (
                    lastest_ask := orderbook["asks"][0][0]
                ):
                    ticker = await self.exchange.fetch_ticker(symbol)
                    logger.info(f"Filtering bid {lastest_bid} > ask {lastest_ask}")
                    if lastest_bid > ticker["bid"]:
                        logger.info(
                            f"Filtering bid {lastest_bid} > ticker bid {ticker['bid']}"
                        )
                        orderbook["bids"].store(lastest_bid, 0)
                    if lastest_ask < ticker["ask"]:
                        logger.info(
                            f"Filtering ask {lastest_ask} < ticker ask {ticker['ask']}"
                        )
                        orderbook["asks"].store(lastest_ask, 0)

                bids, asks = np.array(orderbook["bids"]), np.array(orderbook["asks"])
                timestamp = self.round_milliseconds(orderbook["timestamp"], 60 * 1000)
                bas = BidAskSum(
                    exchange=self._exchange,
                    symbol=symbol,
                    timestamp=timestamp,
                    datetime=self.exchange.iso8601(timestamp),
                    bids_sum_5=float(bids[bids[:, 0] > (bids[0, 0] * 0.95), 1].sum()),
                    bids_sum_10=float(bids[bids[:, 0] > (bids[0, 0] * 0.90), 1].sum()),
                    bids_sum_15=float(bids[bids[:, 0] > (bids[0, 0] * 0.85), 1].sum()),
                    bids_sum_20=float(bids[bids[:, 0] > (bids[0, 0] * 0.80), 1].sum()),
                    asks_sum_5=float(asks[asks[:, 0] < (asks[0, 0] * 1.05), 1].sum()),
                    asks_sum_10=float(asks[asks[:, 0] < (asks[0, 0] * 1.10), 1].sum()),
                    asks_sum_15=float(asks[asks[:, 0] < (asks[0, 0] * 1.15), 1].sum()),
                    asks_sum_20=float(asks[asks[:, 0] < (asks[0, 0] * 1.20), 1].sum()),
                )
                bas_data.append(bas)
                ob_data.append(
                    Orderbook(
                        exchange=self._exchange,
                        symbol=symbol,
                        timestamp=timestamp,
                        datetime=self.exchange.iso8601(timestamp),
                        bids=orderbook["bids"],
                        asks=orderbook["asks"],
                    )
                )
            with db.Session() as session:
                self._insert(ob_data, session, Orderbook)
                self._insert(bas_data, session, BidAskSum)
                session.commit()

            await asyncio.sleep(30)

    def fetch_orderbook_snapshot(
        self, symbols: list[str], session: Session
    ) -> dict[str, _Orderbook]:
        logger.info("Fetching orderbook snapshot")
        tb = self.TABLE
        snapshots = (
            session.query(tb.symbol, tb.bids, tb.asks)
            .distinct(tb.symbol)
            .filter(
                tb.exchange == self._exchange,
                tb.symbol.in_(symbols),
                tb.timestamp
                >= (datetime.now().timestamp() * 1000) - 10 * 60 * 1000,  # 10 minutes
            )
            .order_by(tb.symbol, tb.timestamp.desc())
            .all()
        )
        return {
            snapshot.symbol: self.exchange.order_book(
                {"bids": snapshot.bids, "asks": snapshot.asks}
            )
            for snapshot in snapshots
        }

    async def fetch_data(self):
        pass

    async def backfill_data(self, **kwargs):
        pass
