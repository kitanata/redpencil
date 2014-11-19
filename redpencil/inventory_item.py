class InventoryItem:

    def __init__(self, price=0, days_last_changed=0):
        self._price = price
        self._days_since_price_changed = days_last_changed
        self._promotion_active = False
        self._days_promotion_active = 0

    def set_price(self, price):
        self._promotion_active = self.check_promotion(
            self._price, 
            price,
            self._days_since_price_changed
        )

        self._price = price
        self._days_since_price_changed = 0


    def price_drop_ratio(self, old_price, new_price):
        return round(1 - (new_price / old_price), 2)

    def in_promotion(self):
        return self._promotion_active

    def check_promotion(self, old_price, new_price, days_last_changed):
        if old_price == 0:
            return False

        if days_last_changed < 30:
            return False

        price_drop_ratio = self.price_drop_ratio(old_price, new_price)

        if price_drop_ratio > 0.30:
            return False

        if price_drop_ratio >= 0.05:
            return True

        return False
