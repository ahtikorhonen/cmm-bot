import gzip
import json
import websockets
from typing import Coroutine, Union

import orjson

from src.exchanges.htx_order_book import HTXOrderBook

class HTXDataFeed:
        
    def __init__(self, htx_order_book: HTXOrderBook, depth=150) -> None:
        self.htx_order_book = htx_order_book
        self.symbol = htx_order_book.symbol.lower()
        self.ws_endpoint = "wss://api.huobi.pro/ws"
        self.topics = [f"market.{self.symbol}.depth.step0",
                       f"market.{self.symbol}.mbp.{depth}"]
        self.reqs = [{"req": self.topics[0], "id": "id1"},
                     {"sub": self.topics[1], "id": "id2"}]
        self.reqs_json = [json.dumps(topic) for topic in self.reqs]
    
    async def run(self) -> Union[Coroutine, None]:
        """
        Listens for messages on the WebSocket and updates htx order book.
        """
        async for websocket in websockets.connect(self.ws_endpoint):
            
            self.htx_order_book.is_connected = True
            try:
                for req in self.reqs_json:
                    await websocket.send(req)

                while True:
                    recv = orjson.loads(gzip.decompress(await websocket.recv()))
                    
                    if "ch" in recv:
                        self.htx_order_book.process(recv["tick"])
                        continue
                    elif "ping" in recv:
                        await websocket.send(json.dumps({"ping": recv["ping"]}))
                        continue
                    elif "rep" in recv:
                        self.htx_order_book._initialize(recv["data"])
                    
            except websockets.ConnectionClosed:
                continue

            except Exception as e:
                raise Exception(f"Error with HTX data feed - {e}")
                    