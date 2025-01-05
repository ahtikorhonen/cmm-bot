from typing import Coroutine, Union

from aiohttp import ClientSession
from msgspec.json import Decoder, Encoder

from src.order_book import OrderBook
from src.data_feeds.schema import MsgSchema
from src.parameters import mm_parameters
from c_funcs.build_lib import list_list_str_to_float


class DataFeed:
    """
    Base class for all exchange specifc datafeeds.
    The class contains all general functionality needed for subscribing
    to exchange specific websockets.
    """
    
    json_decoder = Decoder(MsgSchema)
    json_encoder = Encoder()
    
    def __init__(self, order_book: OrderBook): # TODO: implement parser class, handle ob snapshot
        self.session = ClientSession()
        self.order_book = order_book
        self.symbol = mm_parameters["symbol"]
        self.depth = mm_parameters["order_book_depth"]
        
    def parse_order_book_update(self, msg) -> None:
        asks = list_list_str_to_float.parse(msg.data.a)
        bids = list_list_str_to_float.parse(msg.data.b)
        
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