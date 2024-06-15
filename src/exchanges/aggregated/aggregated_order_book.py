import numpy as np

class AggregatedOrderBook():
    """
    Aggregates order books from multiple exchanges into a single order book.
    
    Attributes
    :bids (NDArray): holds the bids for all price levels. Each row is represented by a (prize, size) pair.
    :asks (NDArray): holds the asks for all price levels. Each row is represented by a (prize, size) pair.
    
    Methods
    get_ob_imbalance():
    get_mid_price():
    get_vwmid():
    update_ob():
    """
    
    def __init__(self) -> None:
        """
        Initializes the empty aggregated orderbook.
        """
        self.bids = np.empty((0, 2), dtype=np.float64)
        self.asks = np.empty((0, 2), dtype=np.float64)