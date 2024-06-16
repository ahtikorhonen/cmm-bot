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
        :recv (Dict): the incoming message containing either a snapshot or delta.
        """
        asks = np.array(recv["data"]["a"], dtype=float)
        bids = np.array(recv["data"]["b"], dtype=float)
        
        if recv["type"] == "snapshot":
            self.process_snapshot(bids, asks)
            
        elif recv["type"] == "delta":
            self.asks = self.update(self.asks, asks)
            self.bids = self.update(self.bids, bids)
            self.sort()
                
    def process_bba(self, recv: Dict):
        """
        Handles incoming WebSocket messages to update the best bids and asks.

        Parameters
        :recv (Dict): the incoming message containing latest best bids and asks.
        """
        best_ask = recv["data"]["a"]
        best_bid = recv["data"]["b"]
        
        if best_bid:
            price, quantity = list(map(float, best_bid[0]))
            if quantity > 0:
                self.bba[0, 0] = price
                self.bba[0, 1] = quantity

        if best_ask:
            price, quantity = list(map(float, best_ask[0]))
            if quantity > 0:
                self.bba[1, 0] = price
                self.bba[1, 1] = quantity
