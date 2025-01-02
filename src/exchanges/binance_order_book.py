import numpy as np

from src.base_order_book import BaseOrderBook


class BinanceOrderBook(BaseOrderBook):
            
    def process(self, msg: dict) -> None:
        """
        Handles incoming WebSocket messages to update the order book.
        :msg (dict): the incoming message containing order book updates
        """        
        asks = np.array(msg["a"], dtype=float)
        bids = np.array(msg["b"], dtype=float)
        
        self.asks = self.update(self.asks, asks)
        self.bids = self.update(self.bids, bids)
        self.sort()