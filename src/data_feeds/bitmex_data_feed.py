import json
import orjson
import websockets
from typing import Coroutine, Union

from src.market_data import MarketData

class BitmexDataFeed:
        
    def __init__(self, market_data: MarketData, depth=200) -> None:
        self.market_data = market_data
        self.endpoint = "wss://ws.bitmex.com/realtime"
        self.req = json.dumps({"op": "subscribe", "args": [f"orderBookL2:{self.market_data.symbol}"]})
    
    async def run(self) -> Union[Coroutine, None]:
        """
        Listens for messages on the WebSocket and updates market data.
        """
        async for websocket in websockets.connect(self.endpoint):
            
            self.market_data.bitmex_connected = True
            try:
                await websocket.send(self.req)

                while True:
                    recv = orjson.loads(await websocket.recv())
                    
                    if "action" in recv:
                        if recv["action"] == "partial":
                            print(recv["data"])

            except websockets.ConnectionClosed:
                continue

            except Exception as e:
                raise Exception(f"Error with bitmex data feed - {e}")