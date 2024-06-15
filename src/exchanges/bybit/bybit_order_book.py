from base_order_book import BaseOrderBook

class BybitOrderBook(BaseOrderBook):
    def fill_ob(self, bids, asks):
        self.bids = bids
        self.asks = asks
        self.sort()