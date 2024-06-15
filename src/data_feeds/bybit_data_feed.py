import json
import orjson
import websockets
from typing import Coroutine, Union

from src.market_data import MarketData

class BybitDataFeed:
        
    def __init__(self, market_data: MarketData, depth=200) -> None:
        self.market_data = market_data
        self.endpoint = f"wss://stream.bybit.com/v5/public/spot"
        self.req = json.dumps({"op": "subscribe", "args": [f"orderbook.{depth}.{self.market_data.symbol}"]})
    
    async def run(self) -> Union[Coroutine, None]:
        """
        Listens for messages on the WebSocket and updates market data.
        """
        async for websocket in websockets.connect(self.endpoint):
            self.market_data.bybit_connected = True

            try:
                await websocket.send(self.req)

                while True:
                    recv = orjson.loads(await websocket.recv())
                    
                    if "success" in recv:
                        continue
                    
                    self.market_data.bybit_ob.process(recv)

            except websockets.ConnectionClosed:
                continue

            except Exception as e:
                raise Exception(f"Error with bybit data feed - {e}")