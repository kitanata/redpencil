import sure
import unittest

from redpencil import Inventory, InventoryItem

class TestInventory(unittest.TestCase):

    def setUp(self):
        self.subject = Inventory()

    def test_it_should_have_a_list_of_inventory(self):
        self.subject._items.should.equal([])

    def test_it_should_check_for_promotions(self):
        self.subject.check_for_promotions().should.equal(True)

    def test_it_should_let_us_add_new_items(self):
        self.subject.add_item(InventoryItem(25, 30))

    def test_it_should_not_let_us_specify_invalid_items_when_we_add_them(self):
        self.subject.add_item.when.called_with([]).should.throw(ValueError)
        self.subject.add_item.when.called_with("").should.throw(ValueError)
        self.subject.add_item.when.called_with(5).should.throw(ValueError)
        self.subject.add_item.when.called_with({}).should.throw(ValueError)

    def test_it_should_create_a_promotion_if_the_price_drops_5_percent_or_more(self):
        item = InventoryItem(25, 30)
        self.subject.add_item(item)
        item.set_price(23)
        self.subject.check_for_promotions()
        item.in_promotion().should.equal(True)
