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
        self.endpoint = "wss://api.huobi.pro/ws"
        self.topics = [f"market.{self.symbol}.depth.step0",
                       f"market.{self.symbol}.mbp.{depth}",
                       f"market.{self.symbol}.bbo"]
        self.reqs = [{"req": self.topics[0], "id": "id1"},
                        {"sub": self.topics[1], "id": "id2"},
                        {"sub": self.topics[2], "id": "id3"}]
        self.reqs_json = [json.dumps(topic) for topic in self.reqs]
        self.topic_map = {self.topics[0]: self.htx_order_book._initialize,
                          self.topics[1]: self.htx_order_book.process,
                          self.topics[2]: self.htx_order_book.process_bba}
    
    async def run(self) -> Union[Coroutine, None]:
        """
        Listens for messages on the WebSocket and updates htx order book attributes.
        """
        async for websocket in websockets.connect(self.endpoint):
            
            self.htx_order_book.is_connected = True
            try:
                for req in self.reqs_json:
                    await websocket.send(req)

                while True:
                    recv = orjson.loads(gzip.decompress(await websocket.recv()))
                    
                    if "ping" in recv:
                        req = json.dumps({"pong": recv["ping"]})
                        await websocket.send(req)
                        continue
                    
                    recv_handler = None
                    
                    if "ch" in recv:
                        recv_handler = self.topic_map.get(recv["ch"])
                    elif "rep" in recv:
                        recv_handler = self.topic_map.get(recv["rep"])
                                        
                    if recv_handler:
                        recv_handler(recv)                    
                    
            except websockets.ConnectionClosed:
                continue

            except Exception as e:
                raise Exception(f"Error with HTX data feed - {e}")
                    