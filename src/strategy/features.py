import numpy as np
from numba import njit, float64, prange


@njit(float64(float64[:,:], float64[:,:]), cache=True)
def vwmid(bids: np.ndarray, asks: np.ndarray) -> float:
    """
    Calculate the volume weighted mid price for a given orderbook
    :bids (np.ndarray): represents the bids in a lob with two columns, prize and size
    :asks (np.ndarray): represents the asks in a lob with two columns, prize and size
    :return (float): the volume weighted mid price
    """
    try:
        vwap_bids = np.sum(bids[:, 0] * bids[:, 1]) / np.sum(bids[:, 1])
        vwap_asks = np.sum(asks[:, 0] * asks[:, 1]) / np.sum(asks[:, 1])

        # Compute the volume-weighted mid-price
        volume_weighted_mid_price = (vwap_bids + vwap_asks) / 2

        return volume_weighted_mid_price
    
    except Exception:
        raise Exception("Failed to compute mid-price")

@njit(float64(float64[:, :], float64[:, :], float64), parallel=True, nogil=True, cache=True)
def calculate_vw_mid_with_threshold(bids, asks, volume_threshold):
    """
    Calculate the volume weighted mid price for a given orderbook until a certain volume threshold
    :bids (np.ndarray): represents the bids in a lob with two columns, prize and size
    :asks (np.ndarray): represents the asks in a lob with two columns, prize and size
    :volume_threshold (float): volume threshold for calculating the mid price
    :return (float): the volume weighted mid price
    """
    def vwap_with_threshold(levels, threshold):
        accumulated_volume = 0.0
        weighted_sum = 0.0

        for i in prange(levels.shape[0]):
            price = levels[i, 0]
            volume = levels[i, 1]

            if accumulated_volume + volume > threshold:
                remaining_volume = threshold - accumulated_volume
                weighted_sum += price * remaining_volume
                accumulated_volume += remaining_volume
                break
            else:
                weighted_sum += price * volume
                accumulated_volume += volume

        try:
            return weighted_sum / accumulated_volume
        except Exception:
            raise Exception("Failed to compute mid-price")

    vwap_bids = vwap_with_threshold(bids, volume_threshold)
    vwap_asks = vwap_with_threshold(asks, volume_threshold)
    
    volume_weighted_mid_price = (vwap_bids + vwap_asks) / 2
    
    return volume_weighted_mid_price