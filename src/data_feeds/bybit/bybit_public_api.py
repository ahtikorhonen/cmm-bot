from pybit.unified_trading import HTTP

from src.parameters import parameters


class BybitPublicAPI:
    
    def __init__(self, api_key, api_secret):
        self.category = parameters.CATEGORY
        self.symbol = parameters.SYMBOL
        self.session = HTTP(api_key=api_key, api_secret=api_secret)
    
    def instrument_info(self):
        """
        Fetches instrument information for the specified symbol
        :return (dict): 
        """
        return self.session.get_instruments_info(
            category=self.category,
            symbol=self.symbol
        )
