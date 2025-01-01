import asyncio

from src.strategy.oms import OMS
from src.strategy.marketmaker import MarketMaker


class Strategy:
    def __init__(self, market_data):
        self.market_data = market_data
    
    async def init_ws_connections(self):
        """
        Wait 10 seconds for orderbooks to initialize and then check that both websocket connections are alive
        before starting to quote.
        :return (bool): True if all connections are alive, False otherwise
        """
        await asyncio.sleep(10)
        bybit_is_connected = self.market_data.bybit_order_book.is_connected
        binance_is_connected = self.market_data.binance_order_book.is_connected
        
        return bybit_is_connected and binance_is_connected
                
    async def run(self):
        """
        continuously calculates quotes based on current order book states.
        """
        await self.init_ws_connections()
        
        market_maker = MarketMaker(self.market_data)
        oms = OMS({})
        
        while True:
            await asyncio.sleep(1)
            bid, ask = market_maker.get_quotes()
            #print(f"vol: {vol}")
            await oms.run(bid, ask)
