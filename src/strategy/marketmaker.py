from src.strategy.features import vw_mid
from src.parameters import mm_parameters
from utils.jit_funcs import nbround


class MarketMaker:
    """
    Calculates fair value, spread and skew based on current order book states, past volatility and inventory
    """
    def __init__(self, market_data):
        self.market_data = market_data
        self.min_spread = mm_parameters["min_spread"]

    def get_quotes(self):
        """
        TODO: document
        """
        fair_value = self.fair_value()
        spread = self.spread()
        skew = self.skew()
        
        bid = fair_value - spread + skew
        ask = fair_value + spread + skew
        
        return bid, ask
        
    def skew(self) -> float:
        """
        Calculate skew based on current inventory
        TODO: implement
        """
        return 0
    
    def spread(self) -> float:
        """
        Scales spread based on short-term volatility. The volatility
        is scaled using a linear model that was fitted to historical order book data.
        the model coefficients are, slope = 0.432667 and intercept = 1 which is the tick size.
        Note that this model was fitted to ETHUSDT data and more volatility instruments
        probably require more aggressive scaling.
        :return (float): volatility scaled spread
        """
        spread = nbround(self.tick_size + 0.432667 * self.market_data.mid_prices.vol(),2)
        print(spread)

        return spread
        
    def fair_value(self) -> float:
        """
        Calculate the fair value of an instrument as the mean
        between the 1mm usd volume weighted mid prices on bybit and binance
        """
        bybit_vwmid = vw_mid(self.market_data.bybit_order_book.bids, self.market_data.bybit_order_book.asks, 250.0)
        binance_vwmid = vw_mid(self.market_data.binance_order_book.bids, self.market_data.binance_order_book.asks, 250.0)
        
        return bybit_vwmid * 0.67 + binance_vwmid * 0.33