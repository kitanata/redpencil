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

    def test_it_should_let_us_set_price_and_duration_on_init(self):
        self.other_subject = InventoryItem(25, 30)
        self.other_subject._price.should.equal(25)
        self.other_subject._days_since_price_changed.should.equal(30)

    def test_it_should_let_us_set_a_new_price(self):
        self.subject.set_price(25)
        self.subject._price.should.equal(25)

    def test_it_should_update_price_changed_when_price_is_set(self):
        self.subject = InventoryItem(25, 30)
        self.subject.set_price(20)
        self.subject._days_since_price_changed.should.equal(0)
