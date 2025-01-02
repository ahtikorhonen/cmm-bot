import numpy as np

from src.base_order_book import BaseOrderBook


class BybitOrderBook(BaseOrderBook):
    
    def process_snapshot(self, bids, asks):
        self.bids = bids
        self.asks = asks
        self.sort()
                
    def process(self, msg: dict) -> None:
        """
        Handles incoming WebSocket messages to update the order book.
        :msg (dict): the incoming message containing either a snapshot or delta.
        """
        asks = np.array(msg["data"]["a"], dtype=float)
        bids = np.array(msg["data"]["b"], dtype=float)
        
        if msg["type"] == "snapshot":
            self.process_snapshot(bids, asks)
            
        elif msg["type"] == "delta":
            self.asks = self.update(self.asks, asks)
            self.bids = self.update(self.bids, bids)
            self.sort()

