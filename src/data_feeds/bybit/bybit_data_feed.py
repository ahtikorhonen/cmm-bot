from typing import Coroutine, Union

from aiohttp import WSMsgType

from src.order_book import OrderBook
from src.data_feeds.data_feed import DataFeed
from src.data_feeds.bybit.endpoints import WS_ENDPOINT
from utils.circular_buffer import CircularBuffer


class BybitDataFeed(DataFeed):
    
    __bybit_topics__ = ["Orderbook", "BBA"]

    def __init__(self, order_book: OrderBook, mid_prices: CircularBuffer) -> None:
        super().__init__(order_book)
        self.mid_prices = mid_prices
        self.ws_endpoint, self.topics = self.format_ws_req()
        self.topic_map = {self.topics[0]: self.parse_order_book_update, self.topics[1]: self.process_bba}
        self.req = self.json_encoder.encode({"op": "subscribe", "args": self.topics})
        
    def format_ws_req(self) -> tuple[str, list[str]]:
        url = WS_ENDPOINT
        topics = []
        
        for topic in self.__bybit_topics__:
            stream = ""
            match topic:
                case "Orderbook":
                    stream = f"orderbook.{self.depth}.{self.symbol}"
                case "BBA":
                    stream = f"orderbook.1.{self.symbol}"
                case _:
                    raise ValueError(f"Invalid topic '{topic}' for Bybit websocket feed")
                
            if stream:
                topics.append(stream)
        
        return url, topics

    async def run(self) -> Union[Coroutine, None]:
        async with self.session.ws_connect(self.ws_endpoint) as websocket:
            
            self.order_book.is_connected = True
            
            try:
                await websocket.send_bytes(self.req)

                async for msg in websocket:
                    if msg.type == WSMsgType.TEXT:
                                                
                        recv = self.json_decoder.decode(msg.data)
                                                
                        if recv.topic:
                            topic_handler = self.topic_map[recv.topic]
                            topic_handler(recv)

                    elif msg.type == WSMsgType.ERROR:
                        break

            except Exception as e:
                raise Exception(f"Error with Bybit data feed - {e}")
    
    # TODO: move these to circular_buffer class
    def process_bba(self, recv):
        best_bid = recv.data.b
        best_ask = recv.data.a
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