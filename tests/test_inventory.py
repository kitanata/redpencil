import sure
import unittest

from redpencil import Inventory

class TestInventory(unittest.TestCase):

    def setUp(self):
        self.subject = Inventory()

    def test_it_should_have_a_list_of_inventory(self):
        self.subject._items.should.equal([])

