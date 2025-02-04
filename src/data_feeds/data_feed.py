from typing import Coroutine, Union

from src.order_book import OrderBook
from src.parameters import parameters
from c_funcs.build_lib import list_list_str_to_float


class DataFeed:
    """
    Base class for all exchange specifc datafeeds.
    The class contains all general functionality needed for subscribing
    to exchange specific websockets.
    """
    def __init__(self, order_book: OrderBook):
        self.order_book = order_book
        self.symbol = parameters.SYMBOL
        self.depth = parameters.ORDER_BOOK_DEPTH
        self.topic_map = {}
        
    def handle_recv(self, topic: str, data: dict) -> None:
        """
        Parses the bid and ask arrays and proccesses the new data
        """
        topic_handler = self.topic_map.get(topic)
        
        if topic_handler:
            bids = list_list_str_to_float.parse(data["b"])
            asks = list_list_str_to_float.parse(data["a"])
            topic_handler(bids, asks)
        
    def format_ws_req(self) -> tuple[str, list[str]]:
        """
        Formats a websocket request to specified public topics
        :return (tuple[str, list[str]]): returns a websocket url and a list of topics to subscribe
        """
        raise NotImplementedError("Exchange specific children classes should define this method")
                
    def run(self) -> Union[Coroutine, None]:
        """
        Listens for messages on the WebSocket and updates the exchange specific order book.
        """
        raise NotImplementedError("Exchange specific children classes should define this method")