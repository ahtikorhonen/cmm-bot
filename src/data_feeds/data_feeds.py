import asyncio

from src.market_data import MarketData
from src.data_feeds.bybit_data_feed import BybitDataFeed
from src.data_feeds.bitmex_data_feed import BitmexDataFeed

class DataFeeds:
    
    def __init__(self, market_data: MarketData) -> None:
        self.market_data = market_data
        
    async def start_feeds(self) -> None:
        """
        Starts the WebSocket data feeds.
        """
        tasks = [
            asyncio.create_task(BybitDataFeed(self.market_data).run()),
            #asyncio.create_task(BitmexDataFeed(self.market_data).run())
        ]
        
        await asyncio.gather(*tasks)
