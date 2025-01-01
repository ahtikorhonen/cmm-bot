import json
from typing import Coroutine, Union

import aiohttp
from orjson import loads

from src.exchanges.bybit_order_book import BybitOrderBook
from src.data_feeds.data_feed import DataFeed
from src.data_feeds.endpoints import BYBIT_WS_ENDPOINT
from utils.circular_buffer import CircularBuffer


class BybitDataFeed(DataFeed):

    def __init__(self, order_book: BybitOrderBook, mid_prices: CircularBuffer) -> None:
        super().__init__(order_book)
        self.mid_prices = mid_prices
        self.topics = [f"orderbook.{self.depth}.{self.symbol}"] #, f"orderbook.1.{self.symbol}"]
        self.topic_map = {self.topics[0]: self.order_book.process} #, self.topics[1]: self.process_bba}
        self.req = json.dumps({"op": "subscribe", "args": self.topics})

    async def run(self) -> Union[Coroutine, None]:
        """
        Listens for messages on the WebSocket and updates the Bybit order book.
        """
        async with self.session.ws_connect(BYBIT_WS_ENDPOINT) as websocket:
            
            self.order_book.is_connected = True
            
            try:
                await websocket.send_str(self.req)

                async for msg in websocket:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        recv = loads(msg.data)
                                                
                        if "topic" in recv:
                            topic_handler = self.topic_map[recv["topic"]]
                            topic_handler(recv)

                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        break

            except aiohttp.ClientConnectionError as e:
                await websocket.send_str(self.req)

            except Exception as e:
                raise Exception(f"Error with Bybit data feed - {e}")
    
    def process_bba(self, recv):
        best_bid = recv["data"]["b"]
        best_ask = recv["data"]["a"]
        bb = self.parse_bba(best_bid)
        ba = self.parse_bba(best_ask)

        self.mid_prices.process_bba(bb, ba)
        
    def parse_bba(self, tick):
        price = 0
        
        if tick:
            if len(tick) == 2:
                price = float(tick[0][0]) if float(tick[0][1]) != 0 else float(tick[1][0])
            else:
                price = float(tick[0][0])
        
        return price