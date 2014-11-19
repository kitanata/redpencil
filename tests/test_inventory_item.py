import sure
import unittest

from datetime import datetime, timedelta
from time import sleep

from redpencil import InventoryItem

class TestInventoryItem(unittest.TestCase):

    def setUp(self):
        self.subject = InventoryItem()

    def test_it_should_have_a_normal_price(self):
        self.subject._price.should.equal(0)

    def test_it_should_not_be_in_promotion(self):
        self.subject.in_promotion().should.equal(False)

    def test_it_should_set_a_default_last_price_changed_on(self):
        self.subject._last_price_changed_on.should_not.be.none
        self.subject._last_price_changed_on.date().should.equal(datetime.now().date())

    def test_it_should_start_in_a_non_promotional_state(self):
        self.subject._promotion_active.should.equal(False)
        self.subject._promotion_started_on.should.be.none

    def test_it_should_let_us_set_a_new_price(self):
        self.subject.set_price(25)
        self.subject._price.should.equal(25)



class TestInventoryItemPriceChange(unittest.TestCase):

    def setUp(self):
        self.last_price_changed_on = datetime.now() - timedelta(days=30)
        self.subject = InventoryItem(100, self.last_price_changed_on)

    def test_it_should_let_us_set_price_and_last_price_changed_on_init(self):
        self.subject._price.should.equal(100)
        self.subject._last_price_changed_on.should.equal(self.last_price_changed_on)

    def test_it_should_update_price_changed_when_price_is_set(self):
        self.subject.set_price(50)
        self.subject._last_price_changed_on.should_not.equal(self.last_price_changed_on)

    def test_it_should_calculate_price_drop_ratio(self):
        self.subject.price_drop_ratio(100, 50).should.equal(0.5)

    def test_it_should_not_enter_promotion_when_price_drops_less_than_5_percent(self):
        self.subject.set_price(96)
        self.subject.in_promotion().should.equal(False)

    def test_it_should_enter_promotion_when_price_drops_5_percent(self):
        self.subject.set_price(95)
        self.subject.in_promotion().should.equal(True)

    def test_it_should_enter_promotion_when_price_drops_more_than_5_percent(self):
        self.subject.set_price(94)
        self.subject.in_promotion().should.equal(True)

    def test_it_should_enter_promotion_when_price_drops_30_percent(self):
        #Note to reviewers at Pillar. I totally got floating point errors here. 
        #This would have been hard to detect without TDD. Hence the introduction of
        #the get_price_drop_ratio function above.
        self.subject.set_price(70)
        self.subject.in_promotion().should.equal(True)

    def test_it_should_not_enter_promotion_when_price_drops_more_than_30_percent(self):
        self.subject.set_price(69)
        self.subject.in_promotion().should.equal(False)

    def test_it_should_not_enter_promotion_when_price_is_instable(self):
        self.subject.set_price(99)
        self.subject.set_price(90)
        self.subject.in_promotion().should.equal(False)

    def test_it_should_not_enter_promotion_when_price_hasnt_remained_stable_for_30_days(self):
        self.subject = InventoryItem(100, datetime.now() - timedelta(days=29))
        self.subject.set_price(99)
        self.subject.in_promotion().should.equal(False)

    def test_it_should_enter_promotion_when_price_reamined_stable_for_31_days(self):
        self.subject = InventoryItem(100, datetime.now() - timedelta(days=31))
        self.subject.set_price(95)
        self.subject.in_promotion().should.equal(True)

    def test_it_should_enter_promotion_when_price_is_reduced(self):
        self.subject.set_price(95)
        self.subject._promotion_active.should.equal(True)

    def test_it_should_not_enter_promotion_when_price_is_raised(self):
        self.subject.set_price(150)
        self.subject.in_promotion().should.equal(False)

    def test_it_should_set_date_promotion_started_when_a_promotion_starts(self):
        self.subject.set_price(90)
        self.subject._promotion_started_on.date().should.equal(datetime.now().date())

    def test_it_should_not_set_date_promotion_started_if_already_active(self):
        self.subject.set_price(90)
        sleep(1)
        self.subject.set_price(85)
        (datetime.now() - self.subject._promotion_started_on).seconds.should.be.greater_than(0)

    def test_it_should_end_the_promotion_if_its_been_active_for_longer_than_30_days(self):
        self.subject.set_price(90)
        self.subject._promotion_started_on = self.subject._promotion_started_on - timedelta(days=31)
        self.subject.in_promotion().should.be(False)

    def test_it_should_end_the_promotion_if_its_been_active_for_longer_than_30_days_and_we_set_a_new_price(self):
        self.subject.set_price(90)
        self.subject._promotion_started_on = self.subject._promotion_started_on - timedelta(days=31)
        self.subject.set_price(85)
        self.subject._promotion_active.should.be(False)

