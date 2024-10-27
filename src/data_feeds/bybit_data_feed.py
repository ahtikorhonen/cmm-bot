import json
from typing import Coroutine, Union

import aiohttp
from orjson import loads

from src.exchanges.bybit_order_book import BybitOrderBook
from src.data_feeds.data_feed import DataFeed


class BybitDataFeed(DataFeed):

    def __init__(self, order_book: BybitOrderBook) -> None:
        super().__init__(order_book, "bybit")
        #self._replacement_map = {"{depth}": self._exchange_ws_details["depth"], "{symbol}": self.symbol}
        self._topics = self.format_topics(self._topics, self._replacement_map)
        self.req = json.dumps({"op": "subscribe", "args": self._topics})

    async def run(self) -> Union[Coroutine, None]:
        """
        Listens for messages on the WebSocket and updates the Bybit order book.
        """
        async with self.session.ws_connect(self._ws_endpoint) as websocket:
            self.order_book.is_connected = True
            try:
                await websocket.send_str(self.req)

                async for msg in websocket:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        recv = loads(msg.data)
                                                
                        if "success" in recv:
                            continue
                        
                        self.order_book.process(recv)

                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        break

            except aiohttp.ClientConnectionError as e:
                # TODO: Handle reconnection logic
                pass

            except Exception as e:
                raise Exception(f"Error with Bybit data feed - {e}")