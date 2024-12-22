import numpy as np
from numba import njit, float64


@njit(float64(float64[:], float64[:], float64), cache=True)
def vwmid(bids: np.ndarray, asks: np.ndarray, volume: float = 1_000_000) -> float:
    """
    Calculate the volume weighted mid price for a given orderbook
    :bids (np.ndarray): represents the bids in a lob with two columns, prize and size
    :asks (np.ndarray): represents the asks in a lob with two columns, prize and size
    :volume (float): 
    """
    pass