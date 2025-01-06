import os

from src.order_book import OrderBook
from utils.circular_buffer import CircularBuffer
from src.data_feeds.bybit.bybit_public_api import BybitPublicAPI
from src.parameters import parameters


class MarketData:
    """
    TODO: document
    """
    def __init__(self) -> None:
        self.api_key = os.getenv("API_KEY")
        self.api_secret = os.getenv("API_SECRET")
        if not self.api_key or not self.api_secret:
            raise ValueError("Missing API key and/or secret!")
        
        self.bybit_public_api = BybitPublicAPI(self.api_key, self.api_secret)
                
        self.bybit_order_book = OrderBook(size=500)
        self.binance_order_book = OrderBook(size=500)
        
        self.current_orders = {}
        self.mid_prices = CircularBuffer(capacity=1000)
        
        self._set_instrument_info_()
        
    def _set_instrument_info_(self):
        instrument_info = self.bybit_public_api.instrument_info()
        try:
            result = instrument_info["result"]["list"][0]
            status = result["status"]
            
            if status != "Trading":
                raise Exception(f"{self.bybit_public_api.symbol} is not trading")
            
            leverage = result["leverageFilter"]
            price = result["priceFilter"]
            size = result["lotSizeFilter"]
            
            parameters.MIN_LEV = leverage["minLeverage"]
            parameters.MAX_LEV = leverage["maxLeverage"]
            parameters.LEV_STEP = leverage["leverageStep"]
            
            parameters.MIN_PRICE = price["minPrice"]
            parameters.MAX_PRICE = price["maxPrice"]
            parameters.TICK_SIZE = price["tickSize"]
            
            parameters.MIN_ORDER_QTY = size["minOrderQty"]
            parameters.QTY_STEP = size["qtyStep"]
        
        except Exception as ex:
            raise Exception(f"Failed to set instrument info - {ex}")
