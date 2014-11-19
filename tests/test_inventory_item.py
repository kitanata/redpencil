import sure
import unittest

from redpencil import InventoryItem

class TestInventoryItem(unittest.TestCase):

    def setUp(self):
        self.subject = InventoryItem()

    def test_it_should_have_a_normal_price(self):
        self.subject._price.should.equal(0)

    def test_it_should_have_a_day_counter_since_price_changed(self):
        self.subject._days_since_price_changed.should.equal(0)

