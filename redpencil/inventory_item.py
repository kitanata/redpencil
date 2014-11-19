class InventoryItem:

    def __init__(self, price=0, days_last_changed=0):
        self._last_price = price
        self._price = price
        self._days_since_price_changed = days_last_changed
        self._in_promotion = False

    def set_price(self, price):
        self._last_price = self._price
        self._price = price
        self._days_since_price_changed = 0

    def in_promotion(self):
        if self._last_price == 0:
            return False

        if 1 - (self._price / self._last_price) > 0.05:
            return True
