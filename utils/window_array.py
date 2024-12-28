import numpy as np
from numba import int32, float64
from numba.experimental import jitclass


spec = [
    ('arr', float64[:]),
    ('capacity', int32),
    ('size', int32),
]

@jitclass(spec)
class WindowArray:
    def __init__(self, capacity=100, dtype=float64):
        """
        A fixed size array for storing mid prices from which volatility is calculated
        """
        self.arr = np.zeros(capacity, dtype)
        self.capacity = capacity
        self.size = 0
        
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
            self.arr = np.roll(self.arr, -1)

    def vol(self):
        """
        Calculate standard deviation of the log differences of the values
        in the array i.e. volatility for prices
        """
        log_diff = np.diff(np.log(self.arr[:self.size]))
        return np.std(log_diff)
    