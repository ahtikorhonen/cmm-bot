import os

import numpy as np
from numpy.typing import NDArray

from src.exchanges.bybit_order_book import BybitOrderBook
from src.exchanges.bitmex_order_book import BitmexOrderBook
from src.exchanges.htx_order_book import HTXOrderBook

class MarketData:
    
    def __init__(self) -> None:
        self.api_key = os.getenv("API_KEY")
        self.api_secret = os.getenv("API_SECRET")
        if not self.api_key or not self.api_secret:
            raise ValueError("Missing API key and/or secret!")
                
        self.bybit_order_book = BybitOrderBook()
        self.bitmex_order_book = BitmexOrderBook()
        self.htx_order_book = HTXOrderBook()
        
    @property
    def bybit_mid(self) -> float:
        best_bid, best_ask = self.bybit_order_book.bba[0][0], self.bybit_order_book.bba[0][0]
        mid = (best_ask + best_bid) / 2
        return mid
    