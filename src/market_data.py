import os

import numpy as np
from numpy.typing import NDArray

from src.exchanges.bybit_order_book import BybitOrderBook
from src.exchanges.binance_order_book import BinanceOrderBook

class MarketData:
    
    def __init__(self) -> None:
        self.api_key = os.getenv("API_KEY")
        self.api_secret = os.getenv("API_SECRET")
        if not self.api_key or not self.api_secret:
            raise ValueError("Missing API key and/or secret!")
                
        self.bybit_order_book = BybitOrderBook()
        self.binance_order_book = BinanceOrderBook()
        
    @property
    def bybit_mid(self) -> float:
        best_bid, best_ask = self.bybit_order_book.bba[0][0], self.bybit_order_book.bba[0][0]
        mid = (best_ask + best_bid) / 2
        return mid
    