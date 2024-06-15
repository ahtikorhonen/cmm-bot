import os

import numpy as np
from numpy.typing import NDArray

from src.exchanges.bybit_order_book import BybitOrderBook
from src.exchanges.bitmex_order_book import BitmexOrderBook

class MarketData:
    
    def __init__(self) -> None:
        self.api_key = os.getenv("API_KEY")
        self.api_secret = os.getenv("API_SECRET")
        if not self.api_key or not self.api_secret:
            raise ValueError("Missing API key and/or secret!")
        
        self.symbol = "ETHUSDT"
        
        self.bybit_connected = False
        self.bybit_ob = BybitOrderBook()
        
        self.bitmex_connected = False
        self.bitmex_ob = BitmexOrderBook()
        
    def bybit_mid(self) -> float:
        best_ask = self.bybit_ob.asks[0][0]
        best_bid = self.bybit_ob.bids[0][0]
        return (best_ask + best_bid) / 2
    