import os

from src.order_book import OrderBook
from utils.circular_buffer import CircularBuffer


class MarketData:
    """
    TODO: document
    """
    
    def __init__(self) -> None:
        self.api_key = os.getenv("API_KEY")
        self.api_secret = os.getenv("API_SECRET")
        if not self.api_key or not self.api_secret:
            raise ValueError("Missing API key and/or secret!")
                
        self.bybit_order_book = OrderBook(size=500)
        self.binance_order_book = OrderBook(size=500)
        
        self.current_orders = {}
        self.mid_prices = CircularBuffer(capacity=1000)
