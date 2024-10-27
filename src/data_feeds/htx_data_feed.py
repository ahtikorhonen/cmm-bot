import gzip
import json
from typing import Coroutine, Union

import aiohttp
from orjson import loads

from src.exchanges.htx_order_book import HTXOrderBook
from src.data_feeds.data_feed import DataFeed


class HTXDataFeed(DataFeed):
        
    def __init__(self, order_book: HTXOrderBook) -> None:
        super().__init__(order_book, "htx")
        self.symbol = order_book.symbol.lower()
        self._replacement_map = {"{depth}": self._exchange_ws_details["depth"], "{symbol}": self.symbol}
        self._topics = self.format_topics(self._topics, self._replacement_map)
        self._reqs = [{"req": self._topics[0], "id": "id1"},
                     {"sub": self._topics[1], "id": "id2"}]
        self.reqs_json = [json.dumps(topic) for topic in self._reqs]

    async def run(self) -> Union[Coroutine, None]:
        """
        Listens for messages on the WebSocket and updates the htx order book.
        """
        async with self.session.ws_connect(self._ws_endpoint) as websocket:
            self.order_book.is_connected = True
            try:
                for req in self.reqs_json:
                    await websocket.send_str(req)

                async for msg in websocket:
                    if msg.type == aiohttp.WSMsgType.BINARY:
                        recv = loads(gzip.decompress(msg.data))
                                                
                        if "ch" in recv:
                            self.order_book.process(recv["tick"])
                            continue
                        elif "ping" in recv:
                            await websocket.send_str(json.dumps({"ping": recv["ping"]}))
                            continue
                        elif "rep" in recv:
                            self.order_book._initialize(recv["data"])

                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        raise Exception(f"HTX WebSocket error: {msg.data}")

            except aiohttp.ClientConnectionError:
                # TODO: Handle reconnection logic
                pass

            except Exception as e:
                raise Exception(f"Error with HTX data feed - {e}")
                    