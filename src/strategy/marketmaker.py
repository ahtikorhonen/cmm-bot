from src.market_data import MarketData
from src.strategy.features import vw_mid
from src.parameters import mm_parameters
from utils.jit_funcs import nbround


class MarketMaker:
    def __init__(self, market_data: MarketData):
        self.market_data = market_data
        self.min_spread = mm_parameters["min_spread"]

    def get_quotes(self) -> tuple[float, float]:
        """
        Calculates fair value, spread and skew based on current order book states, past volatility and inventory
        :return (tuple[float, float]): bid and ask prices to quote
        """
        fair_value = self.fair_value()
        spread = self.spread()
        skew = self.skew()
        
        bid = nbround(fair_value - spread + skew, 2)
        ask = nbround(fair_value + spread + skew, 2)
        
        return bid, ask
        
    def skew(self) -> float:
        """
        Calculate skew based on current inventory
        TODO: implement
        """
        return 0
    
    def spread(self) -> float:
        """
        Linearly scales spread based on short-term volatility
        :return (float): volatility scaled spread
        """
        bps_conversion_factor = 10**-5
        model_slope = 0.5
        
        base_spread = self.min_spread * self.market_data.mid_prices.mid_price() * bps_conversion_factor
        scaled_spread = base_spread + model_slope * self.market_data.mid_prices.vol()

        return scaled_spread
        
    def fair_value(self, dollar_depth: int = 1_000_000) -> float:
        """
        Calculate the fair value of an instrument as the weighted mean
        between the 1mm usd volume weighted mid prices on bybit and binance order books
        :dollar_depth (int): volume threshold until which volume weighted average
                                   price is calculated from both sides of the order book
        :return (float): fair value of the traded instrument
        """
        bybit_vw_mid = self.market_data.bybit_order_book.vw_mid(dollar_depth)
        binance_vw_mid = self.market_data.binance_order_book.vw_mid(dollar_depth)
        
        return bybit_vw_mid * 0.67 + binance_vw_mid * 0.33