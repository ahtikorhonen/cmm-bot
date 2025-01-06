import numpy as np
from numba.types import int32, float64
from numba.experimental import jitclass

from utils.jit_funcs import nbround, nbvol


@jitclass
class CircularBuffer:
    """
    A fixed size array for storing mid prices from which volatility is calculated
    """
    
    arr: float64[:]
    capacity: int32
    size: int32
    bid: float64
    ask: float64
    
    def __init__(self, capacity):
        self.arr = np.zeros(capacity, dtype=np.float64)
        self.capacity = capacity
        self.size = 0
        self.bid = 0
        self.ask = 0
        
    def append(self, value: float) -> None:
        """
        Appends values to the array until full and then starts to slide
        the window when new values arrive keeping the size fixed
        :value (float): new value to append to the tail of the array
        """
        if self.size < self.capacity:
            self.arr[self.size] = value
            self.size += 1
        else:
            self.arr[0] = value
            self.arr = np.roll(self.arr, -1) # TODO: change to nbroll

    def vol(self) -> float:
        """
        Volatility
        """
        return nbvol(self.arr[:self.size])
    
    def update(self, bids: np.ndarray, asks: np.ndarray) -> None:
        """
        Parse new best bid and ask prices, append new mid price to the array
        :bids (np.ndarray): New bid orders data, formatted as [[price, size], ...]
        :asks (np.ndarray): new ask orders data, formatted as [[price, size], ...] 
        """
        if bids.size > 0:
            bids = bids[bids[:,1] != 0.0]
            self.bid = bids[0][0]
        
        if asks.size > 0: 
            asks = asks[asks[:,1] != 0.0]
            self.ask = asks[0][0]
            
        mid_price = nbround((self.bid + self.ask) / 2, 2)
        self.append(mid_price)
        
    @property
    def lts(self) -> float:
        """
        Returns the latest recorded mid price
        """
        return self.arr[self.size - 1]