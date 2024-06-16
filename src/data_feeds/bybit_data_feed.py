import json
import orjson
import websockets
from typing import Coroutine, Union

from src.base_order_book import BaseOrderBook

class BybitDataFeed:
    
    _topics = []
    def __init__(self, bybit_order_book: BaseOrderBook, depth=200) -> None:
        self.bybit_order_book = bybit_order_book
        self.symbol = bybit_order_book.symbol
        self.endpoint = "wss://stream.bybit.com/v5/public/spot"
        self._topics = [f"orderbook.{depth}.{self.symbol}", f"orderbook.1.{self.symbol}"]
        self.req = json.dumps({"op": "subscribe", "args": self._topics})
        self.topic_map = {self._topics[0]: self.bybit_order_book.process,
                          self._topics[1]: self.bybit_order_book.process_bba}
    
    async def run(self) -> Union[Coroutine, None]:
        """
        Listens for messages on the WebSocket and updates bybit order book attributes.
        """
        async for websocket in websockets.connect(self.endpoint):
            
            self.bybit_order_book.is_connected = True
            try:
                await websocket.send(self.req)

                while True:
                    recv = orjson.loads(await websocket.recv())
                    
                    if "success" in recv:
                        continue
                    
                    recv_handler = self.topic_map.get(recv["topic"])
                    
                    if recv_handler:
                        recv_handler(recv)
                        
            except websockets.ConnectionClosed:
                continue

            except Exception as e:
                raise Exception(f"Error with bybit data feed - {e}")