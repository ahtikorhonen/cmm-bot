class OMS:
    """
    Parses and sends quotes asynchronously to Bybit.
    """
    def __init__(self, current_orders):
        self.current_orders = current_orders
    
    async def run(self, bid, ask):
        """
        Hadles order parsing and management asynchronously
        TODO: implement
        """
        pass
    
    def parse_orders(self) -> str:
        """
        Parses orders to be sent to Bybit API
        TODO: implement
        """
        pass
    
    def cancel_all_orders(self) -> None:
        """
        Cancel all live orders
        """