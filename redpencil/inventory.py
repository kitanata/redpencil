from .inventory_item import InventoryItem

class Inventory:

    def __init__(self):
        self._items = []

    def check_for_promotions(self):
        return True

    def add_item(self, item):
        if not isinstance(item, InventoryItem):
            raise ValueError

        self._items.append(item)