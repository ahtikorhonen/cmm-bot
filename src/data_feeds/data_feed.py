from typing import Coroutine, Union
from utils.utils import read_json

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
                
    def run(self) -> Union[Coroutine, None]:
        raise NotImplementedError("Exchange specific children classes should define this method")