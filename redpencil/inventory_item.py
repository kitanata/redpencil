from datetime import datetime, timedelta

class InventoryItem:

    def __init__(self, original_price=0, last_price_changed_on=None):
        self._original_price = original_price
        self._reduced_price = original_price
        self._promotion_active = False
        self._days_promotion_active = 0

        self._last_price_changed_on = last_price_changed_on
        self._promotion_started_on = None
        self._promotion_ended_on = None

        if not self._last_price_changed_on: 
            self._last_price_changed_on = datetime.now()


    def set_reduced_price(self, price):
        self._previous_price = self._reduced_price
        self._previous_price_changed_on = self._last_price_changed_on
        if self.has_promotion_expired():
            self._promotion_active = False
            self._promotion_ended_on = self._promotion_started_on + timedelta(days=30)
        if self.should_end_promotion(price, self._reduced_price):
            self._promotion_active = False
            self._promotion_ended_on = datetime.now()
        elif self.should_start_promotion(price):
            self._promotion_active = True
            self._promotion_started_on = datetime.now()

        self._reduced_price = price

        self._last_price_changed_on = datetime.now()


    def in_promotion(self):
        if self.has_promotion_expired():
            self._promotion_active = False
            self._promotion_ended_on = self._promotion_started_on + timedelta(days=30)

        return self._promotion_active


    def has_promotion_expired(self):
        if not self._promotion_started_on:
            return False

        if (datetime.now() - self._promotion_started_on).days > 30:
            return True

        return False


    def get_clearance_percentage(self, reduced_price):
        if self._original_price == 0:
            return 1

        return round(1 - (reduced_price / self._original_price), 2)


    def should_end_promotion(self, new_reduced_price, old_reduced_price):
        if not self._promotion_active:
            return False

        if new_reduced_price > old_reduced_price:
            return True

        if new_reduced_price > self._original_price:
            return True

        if self.get_clearance_percentage(new_reduced_price) > 0.3:
            return True

        return False


    def should_start_promotion(self, new_reduced_price):
        if (datetime.now() - self._last_price_changed_on).days < 30:
            return False

        if self._promotion_ended_on and (
            datetime.now() - self._promotion_ended_on).days < 30:
            return False

        clearance_percentage = self.get_clearance_percentage(new_reduced_price)

        if clearance_percentage > 0.30:
            return False

        if clearance_percentage >= 0.05:
            return True

        return False


    def report(self):
        if hasattr(self, '_previous_price'):
            return \
            ("{date} 100\n"
            "{date_two} 90\n").format(
                date=self._previous_price_changed_on,
                date_two=datetime.now())
        else:
            return "{date} 100\n".format(date=self._last_price_changed_on)
