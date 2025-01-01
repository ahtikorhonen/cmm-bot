import numpy as np
from numba import njit, float64, prange


@njit(float64(float64[:,:], float64[:,:]), cache=True)
def ob_imb(bids: np.ndarray, asks: np.ndarray) -> float:
    """
    Orderbook imbalance i.e. the ratio of bid volume to the total order book volume.
    Signals the buy/sell pressure in the order book at the moment
    :bids (np.ndarray): represents the bids in a lob with two columns, prize and size
    :asks (np.ndarray): represents the asks in a lob with two columns, prize and size
    :return (float): order book imbalance
    """
    vol_bids = np.sum(bids[:, 1])
    vol_asks = np.sum(asks[:, 1])
    
    return (vol_bids - vol_asks) / (vol_bids + vol_asks)

@njit(float64(float64[:, :], float64[:, :], float64), cache=True)
def vw_mid(bids, asks, volume_threshold):
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

        for i in range(levels.shape[0]):
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
        
    return (vwap_bids + vwap_asks) / 2