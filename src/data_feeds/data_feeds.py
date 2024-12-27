import asyncio

from src.market_data import MarketData
from data_feeds.bybit.bybit_data_feed import BybitDataFeed
from data_feeds.binance.binance_data_feed import BinanceDataFeed

class DataFeeds:
    
    def __init__(self, market_data: MarketData) -> None:
        self.market_data = market_data
        
    async def start_feeds(self) -> None:
        """
        Starts the WebSocket data feeds.
        """
        await asyncio.gather(
            asyncio.create_task(BybitDataFeed(self.market_data.bybit_order_book).run()),
            asyncio.create_task(BinanceDataFeed(self.market_data.binance_order_book).run())
        )
