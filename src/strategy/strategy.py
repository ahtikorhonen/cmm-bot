import asyncio


class Strategy:
    def __init__(self, market_data):
        self.market_data = market_data
    
    async def _check_ws_connections(self):
        """
        Check that both websocket connections are alive on a one second interval.
        :return (bool): True if all connections are alive, False otherwise
        """
        while True:
            await asyncio.sleep(1)
            bybit_is_connected = self.market_data.bybit_order_book.is_connected
            binance_is_connected = self.market_data.binance_order_book.is_connected
            
            if bybit_is_connected and binance_is_connected:
                continue
                
            break
    
    async def run(self):
        """
        continuously calculates quotes based on current orderbook states.
        """
        await self._check_ws_connections()
        while True:
            await asyncio.sleep(1)
            bb, bb_size, ba, ba_size = self.market_data.bybit_bba()
            print(f"Bybit best bid: {bb, bb_size}, Bybit best ask: {ba, ba_size}")
            bb, bb_size, ba, ba_size = self.market_data.binance_bba()
            print(f"Binance best bid: {bb, bb_size}, Binance best ask: {ba, ba_size}")
                            