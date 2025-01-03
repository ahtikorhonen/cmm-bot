from typing import Coroutine, Union

from aiohttp import ClientSession

from src.base_order_book import BaseOrderBook
from src.parameters import mm_parameters


class DataFeed:
    """
    Base class for all exchange specifc datafeeds.
    The class contains all general functionality needed for subscribing
    to exchange specific websockets.
    """    
    def __init__(self, order_book: BaseOrderBook):
        self.session = ClientSession()
        self.order_book = order_book
        self.symbol = mm_parameters["symbol"]
        self.depth = mm_parameters["order_book_depth"]
        
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