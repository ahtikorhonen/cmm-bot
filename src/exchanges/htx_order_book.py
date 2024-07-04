from typing import Dict

import numpy as np

from src.base_order_book import BaseOrderBook

class HTXOrderBook(BaseOrderBook):
    
    def _initialize(self, data):
        """
        Handles the initial request containig the entire order book.

        Parameters
        :data (Dict): the incoming data containing the current bids and asks.
        """
        asks = np.array(data["asks"], dtype=float)
        bids = np.array(data["bids"], dtype=float)

        self.asks = asks
        self.bids = bids
        self.sort()
                
    def process(self, tick: Dict) -> None:
        """
        Handles incoming WebSocket messages to update the order book.

        Parameters
        :tick (Dict): the incoming message containing order book or delta
        """
        asks = np.array(tick["asks"], dtype=float)
        bids = np.array(tick["bids"], dtype=float)
        
        self.asks = self.update(self.asks, asks)
        self.bids = self.update(self.bids, bids)
        self.sort()
        
        print(f"asks: {self.asks.shape[0]}, bids: {self.bids.shape[0]}")

        