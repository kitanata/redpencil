class InventoryItem:

    def __init__(self, price=0, days_last_changed=0):
        self._price = price
        self._days_since_price_changed = days_last_changed

    def set_price(self, price):
        self._price = price
        self._days_since_price_changed = 0
