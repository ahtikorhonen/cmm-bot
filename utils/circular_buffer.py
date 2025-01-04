import numpy as np
from numba.types import int32, float64
from numba.experimental import jitclass

from utils.jit_funcs import nbround


@jitclass
class CircularBuffer:
    """
    A fixed size array for storing mid prices from which volatility is calculated
    """
    
    arr: float64[:]
    capacity: int32
    size: int32
    last_bid: float64
    last_ask: float64
    
    def __init__(self, capacity):
        self.arr = np.zeros(capacity, dtype=np.float64)
        self.capacity = capacity
        self.size = 0
        self.last_bid = 0
        self.last_ask = 0
        
    def append(self, value):
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

    def vol(self):
        """
        Calculate standard deviation of the log differences of the values
        in the array i.e. volatility for mid prices
        """
        log_diff = np.diff(np.log(self.arr[:self.size])) # TODO: implement nbvol
        return np.std(log_diff)
    
    def process_bba(self, bid, ask):
        if bid == 0:
            bid = self.last_bid
        if ask == 0:
            ask = self.last_ask
        
        mid = nbround((bid + ask) / 2, 2)
        self.append(mid)
        self.last_bid = bid
        self.last_ask = ask
        
    def mid_price(self):
        """
        Returns the latest recorded mid price
        """
        return self.arr[self.size - 1]