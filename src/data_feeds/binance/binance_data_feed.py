from typing import Coroutine, Union

from src.order_book import OrderBook
from src.data_feeds.data_feed import DataFeed
from src.data_feeds.binance.endpoints import WS_ENDPOINT
from src.data_feeds.picows_client import SingleWsConnection


class BinanceDataFeed(DataFeed):
    
    __binance_topics__ = ["Orderbook"]

    def __init__(self, order_book: OrderBook) -> None:
        super().__init__(order_book)
        self.symbol = self.symbol.lower()
        self.ws_endpoint, self.topics = self.format_ws_req()
        self.topic_map = {self.topics[0]: self.order_book.update}
        
    def format_ws_req(self) -> tuple[str, list[str]]:
        url = WS_ENDPOINT
        topics = []
        
        for topic in self.__binance_topics__:
            stream = ""
            match topic:
                case "Orderbook":
                    stream = f"{self.symbol}@depth@100ms/"
                case _:
                    raise ValueError(f"Invalid topic '{topic}' for Binance websocket feed")
                
            if stream:
                url += stream
                topics.append(stream[:-1])
        
        return url[:-1], topics
    
    async def run(self) -> Union[Coroutine, None]:
        ws_connection = SingleWsConnection()
        await ws_connection.start(self.ws_endpoint)
        self.order_book.is_connected = True
        
        while ws_connection.running:
            try:
                seq_id, ts, recv = await ws_connection.queue.get()
                topic = recv.get("stream")

                if topic:
                    self.handle_recv(topic, recv["data"])

                ws_connection.queue.task_done()
                
            except Exception as e:
                raise Exception(f"Error while consuming messages - {str(e)}")
