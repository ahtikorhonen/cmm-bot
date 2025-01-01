import json
from typing import Coroutine, Union

import aiohttp
from orjson import loads

from src.exchanges.binance_order_book import BinanceOrderBook
from src.data_feeds.data_feed import DataFeed
from src.data_feeds.endpoints import BINANCE_WS_ENDPOINT


class BinanceDataFeed(DataFeed):

    def __init__(self, order_book: BinanceOrderBook) -> None:
        super().__init__(order_book)
        self.topics = [f"{self.symbol.lower()}@depth@100ms"]
        self.topic_map = {"depthUpdate": self.order_book.process}
        self.req = json.dumps({"method": "SUBSCRIBE", "params": self.topics, "id": 1})

    async def run(self) -> Union[Coroutine, None]:
        """
        Listens for messages on the WebSocket and updates the Binance order book.
        """
        async with self.session.ws_connect(BINANCE_WS_ENDPOINT) as websocket:
            
            self.order_book.is_connected = True

            try:
                await websocket.send_str(self.req)

                async for msg in websocket:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        
                        recv = loads(msg.data)
                                                                                        
                        if "e" in recv:
                            topic_handler = self.topic_map[recv["e"]]
                            topic_handler(recv)
                            continue

                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        break

            except aiohttp.ClientConnectionError as e:
                await websocket.send_str(self.req)

            except Exception as e:
                raise Exception(f"Error with Binance data feed - {e}")
