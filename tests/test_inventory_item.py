import sure
import unittest

from redpencil import InventoryItem

class TestInventoryItem(unittest.TestCase):

    def setUp(self):
        self.subject = InventoryItem()

    def test_it_should_have_a_normal_price(self):
        self.subject.price.should.equal(0)
