import asyncio
import uvloop
from dotenv import load_dotenv
load_dotenv()

from src.market_data import MarketData
from src.data_feeds.data_feeds import DataFeeds
from src.strategy.strategy import Strategy


async def main():
    """
    Initializes the market data object and concurrently refreshes the orderbooks from exchange feeds.
    """
    try:
        market_data = MarketData()
        await asyncio.gather(
            asyncio.create_task(DataFeeds(market_data).start_feeds()),
            asyncio.create_task(Strategy(market_data).run())
        )

    except Exception as e:
        raise Exception(f"Critical exception occured - {str(e)}")

if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(main())