from typing import Coroutine, Union

from aiohttp import ClientSession
import numpy as np

from src.order_book import OrderBook
from src.parameters import mm_parameters


class DataFeed:
    """
    Base class for all exchange specifc datafeeds.
    The class contains all general functionality needed for subscribing
    to exchange specific websockets.
    """    
    def __init__(self, order_book: OrderBook):
        self.session = ClientSession()
        self.order_book = order_book
        self.symbol = mm_parameters["symbol"]
        self.depth = mm_parameters["order_book_depth"]
        
    def parse_order_book_update(self, msg: dict) -> None:
        asks = np.array(msg["data"]["a"], dtype=np.float64)
        bids = np.array(msg["data"]["b"], dtype=np.float64)
        
        self.order_book.update(asks, bids)
        
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