from src.data_feeds.bybit.bybit_public_api import BybitPublicAPI


mm_parameters = {
    "lot_size": 0,
    "tick_size": 0,
    "base_spread": 0,
    "symbol": "ETHUSDT",
    "order_book_depth": 200,
    "min_q": 0,
    "max_q": 0,
}

def update_mm_parameter(key, value):
    try:
        mm_parameters[key] = value
    except KeyError:
        raise KeyError(f"Key '{key}' does not exist.")
    
def initialize_parameters():
    """
    TODO: implement
    """
    pass    