from typing import Dict

import numpy as np
from numpy.typing import NDArray

class BaseOrderBook:
    """
    A base class for maintaining and updating an order book with incoming orders.
    
    Attributes
    :bids (NDArray): stores the bids for all price levels. Each row is represented by a (prize, size) pair.
    :asks (NDArray): stores the asks for all price levels. Each row is represented by a (prize, size) pair.
    """
    
    def __init__(self) -> None:
        """
        Initializes the orderbook with empty bids and asks.
        """
        self.bids = np.empty((0, 2), dtype=np.float64)
        self.asks = np.empty((0, 2), dtype=np.float64)
        self.is_connected = False
        self.symbol = "ETHUSDT"
        
    def update(self, old_bids_or_asks, incoming_bids_or_asks) -> NDArray:
        for price, quantity in incoming_bids_or_asks:
            old_bids_or_asks = old_bids_or_asks[old_bids_or_asks[:, 0] != price]
            
            if quantity > 0:
                old_bids_or_asks = np.vstack((old_bids_or_asks, np.array([price, quantity])))

        return old_bids_or_asks
    
    def sort(self) -> None:
        """
        Sorts the bids in descending order and asks in ascending order by price. Keep only 500 levels.
        """
        self.asks = self.asks[self.asks[:, 0].argsort()][:500]
        self.bids = self.bids[self.bids[:, 0].argsort()[::-1]][:500]
        
    def process(self, recv: Dict) -> None:
        """
        Abstract method for proccessing incoming orderbook data.
        
        Parameters:
        :recv (Dict): data to be processed.
        """
        raise NotImplementedError("Exchange specific children classes should define this method!")
