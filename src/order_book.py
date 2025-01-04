import numpy as np
from numba.types import float64, bool_, int32
from numba.experimental import jitclass

from utils.jit_funcs import nbisin, nbroll


@jitclass
class OrderBook:
    """
    Order book class for maintaining a live order book through a websocket connection
    :_size (int): depth of the order book
    :_bids (np.ndarray): stores the bids for all price levels, each row is represented by a (prize, size) pair
    :_asks (np.ndarray): stores the asks for all price levels, each row is represented by a (prize, size) pair
    :_is_connected (bool): boolean indicating the status of the exchange specific websocket connection
    """
    
    _size: int32
    _bids: float64[:, :]
    _asks: float64[:, :]
    is_connected: bool_
    
    def __init__(self, size: int) -> None:
        """
        Initializes the orderbook with empty bids and asks.
        """
        self._size = size
        self._bids = np.empty((0, 2), dtype=np.float64)
        self._asks = np.empty((0, 2), dtype=np.float64)
        self.is_connected = False
        
    def _sort_bids(self, bids: np.ndarray) -> None:
        """
        Removes entries with matching prices in update, regardless of size, and then
        adds non-zero quantity data from update to the book.

        Sorts the bid orders in descending order of price.

        If the best bid is higher than any asks, remove those asks by:
         - Filling the to-be removed arrays with zeros.
         - Rolling it to the back of the orderbook.
        """
        removed_old_prices = self._bids[~nbisin(self._bids[:, 0], bids[:, 0])]
        new_full_bids = np.vstack(
            (
                removed_old_prices[
                    removed_old_prices[:, 1] != 0.0  # Re-remove zeros incase of overlap
                ],
                bids[bids[:, 1] != 0.0],
            )
        )

        self._bids = new_full_bids[new_full_bids[:, 0].argsort()][::-1][:self._size]

        # Remove overlapping asks.
        if self._bids[0, 0] >= self._asks[0, 0]:
            overlapping_asks = self._asks[self._asks[:, 0] <= self._bids[0, 0]].shape[0]
            self._asks[:overlapping_asks].fill(0.0)
            self._asks[:, :] = nbroll(self._asks, -overlapping_asks, 0)

    def _sort_asks(self, asks: np.ndarray) -> None:
        """
        Removes entries with matching prices in update, regardless of size, and then
        adds non-zero quantity data from update to the book.

        Sorts the ask orders in ascending order of price.

        If the best ask is lower than any bids, remove those bids by:
         - Filling the to-be removed arrays with zeros.
         - Rolling it to the back of the orderbook.
        """
        removed_old_prices = self._asks[~nbisin(self._asks[:, 0], asks[:, 0])]
        new_full_asks = np.vstack(
            (
                removed_old_prices[
                    removed_old_prices[:, 1] != 0.0  # Re-remove zeros incase of overlap
                ],
                asks[asks[:, 1] != 0.0],
            )
        )

        self._asks = new_full_asks[new_full_asks[:, 0].argsort()][: self._size]

        # Remove overlapping bids.
        if self._asks[0, 0] <= self._bids[0, 0]:
            overlapping_bids = self._bids[self._bids[:, 0] >= self._asks[0, 0]].shape[0]
            self._bids[:overlapping_bids].fill(0.0)
            self._bids[:, :] = nbroll(self._bids, -overlapping_bids, 0)
            
    def update(self, asks: np.ndarray, bids: np.ndarray) -> None:
        """
        Updates the order book with new ask and bid data
        :asks (np.ndarray): new ask orders data, formatted as [[price, size], ...]
        :bids (np.ndarray): New bid orders data, formatted as [[price, size], ...]
        """
        if asks.ndim == 2 and asks.shape[0] > 0:
            self._sort_asks(asks)
        
        if bids.ndim == 2 and bids.shape[0] > 0:
            self._sort_bids(bids)
        
    def vw_mid(self, dollar_depth: float) -> float:
        """
        Calculates the volume-weighted mid price up to a specified depth for both bids and asks
        :dollar_depth (float): The depth, in dollars, up to which the mid price is calculated
        :return (float): mid price weighted by order sizes up to the specified depth
        """
        bid_size_weighted_sum = 0.0
        ask_size_weighted_sum = 0.0
        bid_cum_size = 0.0
        ask_cum_size = 0.0

        for price, size in self._bids:
            if bid_cum_size + size > dollar_depth:
                remaining_size = dollar_depth - bid_cum_size
                bid_size_weighted_sum += price * remaining_size
                bid_cum_size += remaining_size
                break

            bid_size_weighted_sum += price * size
            bid_cum_size += size

            if bid_cum_size >= dollar_depth:
                break

        for price, size in self._asks:
            if ask_cum_size + size > dollar_depth:
                remaining_size = dollar_depth - ask_cum_size
                ask_size_weighted_sum += price * remaining_size
                ask_cum_size += remaining_size
                break

            ask_size_weighted_sum += price * size
            ask_cum_size += size

            if ask_cum_size >= dollar_depth:
                break

        vwap_bids = bid_size_weighted_sum / bid_cum_size
        vwap_asks = ask_size_weighted_sum / ask_cum_size

        return (vwap_bids + vwap_asks) / 2

    def imbalance(self) -> float:
        """
        Calculates the Orderbook imbalance, which signals,
        the buy/sell pressure in the order book at the moment
        :return (float): a value between -1 and 1
        """
        vol_bids = np.sum(self._bids[:, 1])
        vol_asks = np.sum(self._asks[:, 1])
        
        return (vol_bids - vol_asks) / (vol_bids + vol_asks)
    
    @property
    def mid_price(self) -> float:
        """
        Calculates the mid price of the order book based on the best bid and ask prices
        :return (float): the mid price, which is the average of the best bid and best ask prices
        """
        return (self._bids[0, 0] + self._asks[0, 0]) / 2.0
    
    @property
    def bid_ask_spread(self) -> float:
        """
        Calculates the current spread of the order book
        :return (float): the spread, defined as the difference between the best ask and the best bid prices
        """
        return self._asks[0, 0] - self._bids[0, 0]
    
    @property
    def bids(self) -> np.ndarray:
        return self._bids

    @property
    def asks(self) -> np.ndarray:
        return self._asks

    @property
    def is_empty(self) -> bool:
        return np.all(self._bids == 0.0) and np.all(self._asks == 0.0)
