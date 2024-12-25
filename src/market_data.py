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
        self.initializing = True
        
        self.orders = {}
        
    def bybit_bba(self) -> float:
        return self.bybit_order_book.bids[0][0], self.bybit_order_book.asks[0][0]
        
    def binance_bba(self) -> float:
        return self.binance_order_book.bids[0][0], self.binance_order_book.asks[0][0]
