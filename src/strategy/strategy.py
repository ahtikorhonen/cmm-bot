import asyncio

from src.strategy.features import vwmid, calculate_vw_mid_with_threshold


class Strategy:
    def __init__(self, market_data):
        self.market_data = market_data
    
    async def _check_ws_connections(self):
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
        await self._check_ws_connections()
        while True:
            await asyncio.sleep(0.1)
            bybit_order_book = self.market_data.bybit_order_book
            binance_order_book = self.market_data.binance_order_book
            bybit_vwmid = calculate_vw_mid_with_threshold(bybit_order_book.bids, bybit_order_book.asks, 250.0)
            binance_vwmid = calculate_vw_mid_with_threshold(binance_order_book.bids, binance_order_book.asks, 250.0)
            print(f"Binance vwmid: {binance_vwmid}, Bybit vwmid: {bybit_vwmid}")
                            