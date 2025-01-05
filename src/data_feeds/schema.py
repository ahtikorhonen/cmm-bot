from msgspec import Struct
from typing import List, Tuple


class OrderbookData(Struct):
    b: List[List[str]]
    a: List[List[str]]
    
class MsgSchema(Struct):
    """
    Schema for both bybit and binance websocket messages related to order book updates.
    defining the schema makes json deserialization faster since it omits unwanted fields
    from the websocket messages.
    """
    data: OrderbookData = []
    topic: str = ""
    type: str = ""
    stream: str = ""
    exchange: str = "bybit" if type else "binance"