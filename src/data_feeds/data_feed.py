from typing import Coroutine, Union
from utils.utils import read_json

from aiohttp import ClientSession

from src.base_order_book import BaseOrderBook


class DataFeed:
    """
    Base class for all exchange specifc datafeeds.
    The class contains all general functionality needed for subscribing
    to exchange specific websockets.
    """
    def __init__(self, order_book: BaseOrderBook, exchange_name: str):
        self.session = ClientSession()
        self.order_book = order_book
        self.symbol = order_book.symbol
        self._exchange_ws_details = self.get_ws_exchange_details(exchange_name)
        self._ws_endpoint = self._exchange_ws_details["ws_endpoint"]
        self._topics = self._exchange_ws_details["topics"]
        self._replacement_map = {"{depth}": self._exchange_ws_details["depth"], "{symbol}": self.symbol}
                
    def get_ws_exchange_details(self, exchange_name: str):
        """
        Fetches exchange specific websocket details from config file.
        :file_name (str): exchange which details we want to get
        :return (dict): dict containing websocket endpoint, list of topics that we want
            to subscribe to from a given exchange and the orderbook depth which we want to receive
        """
        ws_details_dict = read_json("exchange_ws_details")
        try:
            exchange_ws_details = ws_details_dict[exchange_name]
            
            return exchange_ws_details
        
        except KeyError:
            raise KeyError(f"Missing exchange specific websocket details from config")
        
    def format_topics(self, topics: list[str], replacement_map: dict):
        """
        Format topics to exchange specific format.
        :topics (list[str]): the topics that we want to subscribe to from a given exchange
        :replacement_map (dict): dict where keys are substrings to replace and values are the replacement strings
        """
        formatted_topics = []
        for topic in topics:
            for k, v in replacement_map.items():
                topic = topic.replace(k, v)
            
            formatted_topics.append(topic)
        
        return formatted_topics
                
    def run(self) -> Union[Coroutine, None]:
        raise NotImplementedError("Exchange specific children classes should define this method")