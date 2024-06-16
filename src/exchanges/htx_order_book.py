from typing import Dict

import numpy as np

from src.base_order_book import BaseOrderBook

class HTXOrderBook(BaseOrderBook):
    
    def _initialize(self, recv):
        """
        Handles the initial request containig the entire order book.

        Parameters
        :recv (Dict): the incoming data containing the current bids and asks.
        """
        asks = np.array(recv["data"]["asks"], dtype=float)
        bids = np.array(recv["data"]["bids"], dtype=float)

        self.asks = asks
        self.bids = bids
        self.sort()
                
    def process(self, recv: Dict) -> None:
        """
        Handles incoming WebSocket messages to update the order book.

        Parameters
        :recv (Dict): the incoming message containing either a snapshot or delta
        """
        asks = np.array(recv["tick"]["asks"], dtype=float)
        bids = np.array(recv["tick"]["bids"], dtype=float)
        
        self.asks = self.update(self.asks, asks)
        self.bids = self.update(self.bids, bids)
        self.sort()
        
        print(f"bids: {self.bids.shape[0]}, asks: {self.asks.shape[0]}")
        
    def process_bba(self, recv: Dict):
        """
        Handles incoming WebSocket messages to update the best bids and asks.

        Parameters
        :recv (Dict): the incoming message containing latest best bids and asks.
        """
        best_ask, best_ask_size = float(recv["tick"]["ask"]), float(recv["tick"]["askSize"])
        best_bid, best_bid_size = float(recv["tick"]["bid"]), float(recv["tick"]["bidSize"])
        
        self.bba[0, 0] = best_bid
        self.bba[0, 1] = best_bid_size

        self.bba[1, 0] = best_ask
        self.bba[1, 1] = best_ask_size
        