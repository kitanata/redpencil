from .inventory_item import InventoryItem

class Inventory:

    def __init__(self):
        self._items = []

    def check_for_promotions(self):
        for item in self._items:
            if 1 - (item._price / item._last_price) > 0.05:
                item.start_promotion()

        return True

    def add_item(self, item):
        if not isinstance(item, InventoryItem):
            raise ValueError

        self._items.append(item)