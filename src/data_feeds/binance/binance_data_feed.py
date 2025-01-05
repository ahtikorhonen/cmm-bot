from typing import Coroutine, Union

from aiohttp import WSMsgType

from src.order_book import OrderBook
from src.data_feeds.data_feed import DataFeed
from src.data_feeds.binance.endpoints import WS_ENDPOINT


class BinanceDataFeed(DataFeed):
    
    __binance_topics__ = ["Orderbook"]

    def __init__(self, order_book: OrderBook) -> None:
        super().__init__(order_book)
        self.symbol = self.symbol.lower()
        self.ws_endpoint, self.topics = self.format_ws_req()
        self.topic_map = {self.topics[0]: self.parse_order_book_update}
        
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
        async with self.session.ws_connect(self.ws_endpoint) as websocket:
            
            self.order_book.is_connected = True

            try:
                async for msg in websocket:
                    if msg.type == WSMsgType.TEXT:
                        
                        recv = self.json_decoder.decode(msg.data)
                                                                                        
                        if recv.stream:
                            topic_handler = self.topic_map[recv.stream]
                            topic_handler(recv)

                    elif msg.type == WSMsgType.ERROR:
                        break
                    
            except Exception as e:
                raise Exception(f"Error with Binance data feed - {e}")
