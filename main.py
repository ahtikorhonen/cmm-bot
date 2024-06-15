import asyncio
import uvloop
from dotenv import load_dotenv
load_dotenv()

from src.market_data import MarketData
from src.data_feeds.data_feeds import DataFeeds

async def main():
    """
    Initializes the market data object and concurrently refreshes the parameters from exchange feeds.
    """
    try:
        market_data = MarketData()
        await asyncio.gather(
            asyncio.create_task(DataFeeds(market_data).start_feeds())
        )
        
    except Exception as e:
        raise Exception(f"Critical exception occured - {str(e)}")

if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(main())