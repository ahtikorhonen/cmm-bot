import numpy as np

class BaseOrderBook():
    """
    A base class for maintaining and updating an order book with incoming orders.
    
    Attributes
    :bids (NDArray): stores the bids for all price levels. Each row is represented by a (prize, size) pair.
    :asks (NDArray): stores the asks for all price levels. Each row is represented by a (prize, size) pair.
    
    Methods
    sort():
    update():
    proccess():
    """
    
    def __init__(self) -> None:
        """
        Initializes the orderbook with empty bids and asks.
        """
        self.bids = np.empty((0, 2), dtype=np.float64)
        self.asks = np.empty((0, 2), dtype=np.float64)
        
    def sort(self) -> None:
        """
        Sorts the bids in descending order and asks in ascending order by price.
        """
        # Get the indices that would sort the first column in descending order
        self.asks = self.asks[self.asks[:, 0].argsort()]
        self.bids = self.bids[self.bids[:, 0].argsort()[::-1]]