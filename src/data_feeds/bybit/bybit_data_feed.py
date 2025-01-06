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
        self.topic_map = {self.topics[0]: self.order_book.update, self.topics[1]: self.mid_prices.update}
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
                        topic = recv.get("topic")
                        
                        if topic:
                            self.handle_recv(topic, recv["data"])

                    elif msg.type == WSMsgType.ERROR:
                        break

            except Exception as e:
                raise Exception(f"Error with Bybit data feed - {e}")