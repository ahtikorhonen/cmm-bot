import os

from exchanges.bybit.bybit_order_book import BybitOrderBook
from exchanges.bitmex.bitmex_order_book import BitmexOrderBook

class MarketData:
    
    def __init__(self) -> None:
        self.api_key = os.getenv("API_KEY")
        self.api_secret = os.getenv("API_SECRET")
        if not self.api_key or not self.api_secret:
            raise ValueError("Missing API key and/or secret!")
        
        self.bybit_ob = BybitOrderBook()
        self.bitmex_ob = BitmexOrderBook()