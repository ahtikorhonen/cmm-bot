import json
from typing import Coroutine, Union

import aiohttp
from orjson import loads

from src.exchanges.binance_order_book import BinanceOrderBook
from src.data_feeds.data_feed import DataFeed


class BinanceDataFeed(DataFeed):

    def __init__(self, order_book: BinanceOrderBook) -> None:
        super().__init__(order_book, "binance")
        self.symbol = order_book.symbol.lower()
        self._replacement_map = {"{symbol}": self.symbol}
        self._topics = self.format_topics(self._topics, self._replacement_map)
        self.req = json.dumps({"method": "SUBSCRIBE", "params": self._topics, "id": 1})

    async def run(self) -> Union[Coroutine, None]:
        """
        Listens for messages on the WebSocket and updates the Binance order book.
        """
        async with self.session.ws_connect(self._ws_endpoint) as websocket:
            self.order_book.is_connected = True
            try:
                await websocket.send_str(self.req)

                async for msg in websocket:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        recv = loads(msg.data)
                                                
                        if "e" in recv:
                            self.order_book.process(recv)
                        if "ping" in recv:
                            await websocket.send_str(json.dumps({"pong": recv["ping"]}))

                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        break

            except aiohttp.ClientConnectionError as e:
                # TODO: Handle reconnection logic
                pass

            except Exception as e:
                raise Exception(f"Error with Binance data feed - {e}")