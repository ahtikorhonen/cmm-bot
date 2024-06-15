import asyncio
import uvloop
from dotenv import load_dotenv
load_dotenv()

from src.market_data import MarketData

async def main():
    """
    Initializes the market data object and concurrently refreshes the parameters from exchange feeds.
    """
    try:
        market_data = MarketData()
        await asyncio.gather(
            asyncio.create_task()
        )
        
    except Exception as e:
        raise Exception(f"Critical exception occured - {str(e)}")

if __name__ == "__Main__":
    asyncio.run(main())