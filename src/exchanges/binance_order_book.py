from typing import Dict

import numpy as np

from src.base_order_book import BaseOrderBook

class BinanceOrderBook(BaseOrderBook):
    
    '''def initialize(self, data):
        """
        Handles the initial request containing the entire order book.
        :data (Dict): the incoming data containing the current bids and asks.
        """
        asks = np.array(data["asks"], dtype=float)
        asks = asks[asks[:,1] != 0]
        bids = np.array(data["bids"], dtype=float)
        bids = bids[bids[:,1] != 0]

        self.asks = asks
        self.bids = bids
        self.sort()'''
                
    def process(self, msg: Dict) -> None:
        """
        Handles incoming WebSocket messages to update the order book.
        :msg (Dict): the incoming message containing order book updates
        """        
        asks = np.array(msg["a"], dtype=float)
        bids = np.array(msg["b"], dtype=float)
        
        self.asks = self.update(self.asks, asks)
        self.bids = self.update(self.bids, bids)
        self.sort()