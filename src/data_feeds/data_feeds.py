import asyncio

from src.market_data import MarketData
from src.data_feeds.bybit_data_feed import BybitDataFeed
from src.data_feeds.htx_data_feed import HTXDataFeed
from src.data_feeds.binance_data_feed import BinanceDataFeed

class DataFeeds:
    
    def __init__(self, market_data: MarketData) -> None:
        self.market_data = market_data
        
    async def start_feeds(self) -> None:
        """
        Starts the WebSocket data feeds.
        """
        tasks = [
            asyncio.create_task(BybitDataFeed(self.market_data.bybit_order_book).run()),
            #asyncio.create_task(HTXDataFeed(self.market_data.htx_order_book).run()),
            asyncio.create_task(BinanceDataFeed(self.market_data.binance_order_book).run())
        ]
        
        await asyncio.gather(*tasks)
