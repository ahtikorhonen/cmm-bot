from typing import Dict

import numpy as np

from src.base_order_book import BaseOrderBook

class BybitOrderBook(BaseOrderBook):
    
    def process_snapshot(self, bids, asks):
        self.bids = bids
        self.asks = asks
        self.sort()
                
    def process(self, recv: Dict) -> None:
        """
        Handles incoming WebSocket messages to update the order book.

        Parameters
        :recv (Dict): the incoming message containing either a snapshot or delta
        """
        asks = np.array(recv["data"]["a"], dtype=float)
        bids = np.array(recv["data"]["b"], dtype=float)
        
        print()

        if recv["type"] == "snapshot":
            self.process_snapshot(bids, asks)
            
        elif recv["type"] == "delta":
            self.asks = self.update(self.asks, asks)
            self.bids = self.update(self.bids, bids)
            self.sort()