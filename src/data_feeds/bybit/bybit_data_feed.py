from typing import Coroutine, Union

from src.order_book import OrderBook
from src.data_feeds.data_feed import DataFeed
from src.data_feeds.bybit.endpoints import WS_ENDPOINT
from utils.circular_buffer import CircularBuffer
from src.data_feeds.picows_client import SingleWsConnection


class BybitDataFeed(DataFeed):
    
    __bybit_topics__ = ["Orderbook", "BBA"]

    def __init__(self, order_book: OrderBook, mid_prices: CircularBuffer) -> None:
        super().__init__(order_book)
        self.mid_prices = mid_prices
        self.ws_endpoint, self.topics = self.format_ws_req()
        self.topic_map = {self.topics[0]: self.order_book.update, self.topics[1]: self.mid_prices.update}
        self.req = [{"op": "subscribe", "args": self.topics}]
        
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
        ws_connection = SingleWsConnection()
        await ws_connection.start(self.ws_endpoint, self.req)
        self.order_book.is_connected = True
        
        while ws_connection.running:
            try:
                seq_id, ts, recv = await ws_connection.queue.get()
                topic = recv.get("topic")
                
                if topic:
                    self.handle_recv(topic, recv["data"])

                ws_connection.queue.task_done()
                
            except Exception as e:
                raise Exception(f"Error while consuming messages - {str(e)}")