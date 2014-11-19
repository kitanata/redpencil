from datetime import datetime

class InventoryItem:

    def __init__(self, price=0, last_price_changed_on=None):
        self._price = price
        self._promotion_active = False
        self._days_promotion_active = 0

        self._last_price_changed_on = last_price_changed_on
        self._promotion_started_on = None

        if not self._last_price_changed_on: 
            self._last_price_changed_on = datetime.now()


    def days_since_price_changed(self):
        return (datetime.now() - self._last_price_changed_on).days


    def set_price(self, price):
        should_start_promotion = self.should_start_promotion(
            self._price, 
            price,
            self.days_since_price_changed()
        )

        if should_start_promotion:    
            self._promotion_active = True
            self._promotion_started_on = datetime.now()

        self._price = price
        self._last_price_changed_on = datetime.now()


    def in_promotion(self):
        self.check_promotion_is_over()

        return self._promotion_active


    def price_drop_ratio(self, old_price, new_price):
        return round(1 - (new_price / old_price), 2)


    def check_promotion_is_over(self):
        if not self._promotion_active:
            return False

        if (datetime.now() - self._promotion_started_on).days > 30:
            self._promotion_active = False
            return True


    def should_start_promotion(self, old_price, new_price, days_last_changed):
        if old_price == 0:
            return False

        if self.check_promotion_is_over():
            return False

        if new_price > old_price:
            self._promotion_active = False
            return False

        if days_last_changed < 30:
            return False

        price_drop_ratio = self.price_drop_ratio(old_price, new_price)

        if price_drop_ratio > 0.30:
            return False

        if price_drop_ratio >= 0.05:
            return True

        return False
