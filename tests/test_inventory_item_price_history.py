import sure
import unittest

from datetime import datetime, timedelta
from redpencil import InventoryItem

from freezegun import freeze_time

class TestInventoryItemPriceHistory(unittest.TestCase):

    def setUp(self):
        self.last_price_changed_on = datetime.now() - timedelta(days=30)
        self.subject = InventoryItem(100, self.last_price_changed_on)


    def test_it_should_be_able_to_create_a_simple_report(self):
        self.subject.report().should.equal(
            '{date} {price}\n'.format(
                date=self.last_price_changed_on,
                price=100))


    @freeze_time('2014-11-26')
    def test_it_should_be_able_to_create_a_two_entry_report(self):
        self.subject.set_reduced_price(90) 
        self.subject.report().should.equal(
            "{date_one} {price_one}\n"
            "{date_two} {price_two}\n".format(
                date_two=datetime.now(),
                price_two=90,
                date_one=self.last_price_changed_on,
                price_one=100))


    @freeze_time('2014-11-26')
    def test_it_should_be_able_to_create_a_two_entry_report(self):
        self.subject.set_reduced_price(90) 
        self.subject.set_reduced_price(80)
        self.subject.report().should.equal(
            "{date_one} {price_one}\n"
            "{date_two} {price_two}\n"
            "{date_three} {price_three}\n".format(
                date_two=datetime.now(),
                price_two=90,
                date_one=self.last_price_changed_on,
                price_one=100,
                date_three=datetime.now(),
                price_three=80))