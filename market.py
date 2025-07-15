class Market:
    def __init__(self, price_data):
        self.price_data = price_data
        self.current_step = 0

    def step(self):
        """Advance the market by one time step."""
        pass

    def get_current_price(self, symbol):
        """Return the current price for a given stock symbol."""
        pass 