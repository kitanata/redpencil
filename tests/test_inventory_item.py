import sure
import unittest

from datetime import datetime, timedelta
from time import sleep

from redpencil import InventoryItem

class TestInventoryItem(unittest.TestCase):

    def setUp(self):
        self.subject = InventoryItem()

    def test_it_should_have_an_original_price_and_a_reduced_price(self):
        self.subject._original_price.should.equal(0)
        self.subject._reduced_price.should.equal(0)

    def test_it_should_not_be_in_promotion(self):
        self.subject.in_promotion().should.equal(False)

    def test_it_should_set_a_default_last_price_changed_on(self):
        self.subject._last_price_changed_on.should_not.be.none
        self.subject._last_price_changed_on.date().should.equal(datetime.now().date())

    def test_it_should_start_in_a_non_promotional_state(self):
        self.subject._promotion_active.should.equal(False)
        self.subject._promotion_started_on.should.be.none
        self.subject._promotion_ended_on.should.be.none

    def test_it_should_let_us_set_a_new_price(self):
        self.subject.set_reduced_price(25)
        self.subject._reduced_price.should.equal(25)



class TestInventoryItemPriceChange(unittest.TestCase):

    def setUp(self):
        self.last_price_changed_on = datetime.now() - timedelta(days=30)
        self.subject = InventoryItem(100, self.last_price_changed_on)

    def test_it_should_let_us_set_price_and_last_price_changed_on_init(self):
        self.subject._original_price.should.equal(100)
        self.subject._reduced_price.should.equal(100)
        self.subject._last_price_changed_on.should.equal(self.last_price_changed_on)

    def test_it_should_update_price_changed_when_price_is_set(self):
        self.subject.set_reduced_price(50)
        self.subject._last_price_changed_on.should_not.equal(self.last_price_changed_on)

    def test_it_should_calculate_the_clearance_percentage(self):
        self.subject.get_clearance_percentage(50).should.equal(0.5)
        self.subject.get_clearance_percentage(44).should.equal(0.56)
        self.subject.get_clearance_percentage(56).should.equal(0.44)



class TestInventoryItemPromotionStart(unittest.TestCase):
    def setUp(self):
        self.last_price_changed_on = datetime.now() - timedelta(days=30)
        self.subject = InventoryItem(100, self.last_price_changed_on)

    def test_it_should_not_enter_promotion_when_price_drops_less_than_5_percent(self):
        self.subject.set_reduced_price(96)
        self.subject.in_promotion().should.equal(False)

    def test_it_should_enter_promotion_when_price_drops_5_percent(self):
        self.subject.set_reduced_price(95)
        self.subject.in_promotion().should.equal(True)

    def test_it_should_enter_promotion_when_price_drops_more_than_5_percent(self):
        self.subject.set_reduced_price(94)
        self.subject.in_promotion().should.equal(True)

    def test_it_should_enter_promotion_when_price_drops_30_percent(self):
        #Note to reviewers at Pillar. I totally got floating point errors here. 
        #This would have been hard to detect without TDD. Hence the introduction of
        #the get_price_drop_ratio function above.
        self.subject.set_reduced_price(70)
        self.subject.in_promotion().should.equal(True)

    def test_it_should_not_enter_promotion_when_price_drops_more_than_30_percent(self):
        self.subject.set_reduced_price(69)
        self.subject.in_promotion().should.equal(False)

    def test_it_should_not_enter_promotion_when_price_is_instable(self):
        self.subject.set_reduced_price(99)
        self.subject.set_reduced_price(90)
        self.subject.in_promotion().should.equal(False)

    def test_it_should_not_enter_promotion_when_price_hasnt_remained_stable_for_30_days(self):
        self.subject = InventoryItem(100, datetime.now() - timedelta(days=29))
        self.subject.set_reduced_price(99)
        self.subject.in_promotion().should.equal(False)

    def test_it_should_enter_promotion_when_price_remained_stable_for_31_days(self):
        self.subject = InventoryItem(100, datetime.now() - timedelta(days=31))
        self.subject.set_reduced_price(95)
        self.subject.in_promotion().should.equal(True)

    def test_it_should_enter_promotion_when_price_is_reduced(self):
        self.subject.set_reduced_price(95)
        self.subject._promotion_active.should.equal(True)

    def test_it_should_not_enter_promotion_when_price_is_raised(self):
        self.subject.set_reduced_price(150)
        self.subject.in_promotion().should.equal(False)

    def test_it_should_set_date_promotion_started_when_a_promotion_starts(self):
        self.subject.set_reduced_price(90)
        self.subject._promotion_started_on.date().should.equal(datetime.now().date())

    def test_it_should_not_set_date_promotion_started_if_already_active(self):
        self.subject.set_reduced_price(90)
        sleep(1)
        self.subject.set_reduced_price(85)
        (datetime.now() - self.subject._promotion_started_on).seconds.should.be.greater_than(0)



class TestInventoryItemPromotionEnding(unittest.TestCase):
    def setUp(self):
        self.last_price_changed_on = datetime.now() - timedelta(days=30)
        self.subject = InventoryItem(100, self.last_price_changed_on)

    def test_it_should_set_a_date_the_promotion_ended(self):
        self.subject._promotion_ended_on.should.be.none
        self.subject.set_reduced_price(90)
        self.subject.in_promotion().should.be(True)
        self.subject.set_reduced_price(91)
        self.subject.in_promotion().should.be(False)
        self.subject._promotion_ended_on.should_not.be.none

    def test_it_should_end_the_promotion_if_its_been_active_for_longer_than_30_days(self):
        self.subject.set_reduced_price(90)
        self.subject._promotion_started_on = self.subject._promotion_started_on - timedelta(days=31)
        self.subject.in_promotion().should.be(False)

    def test_it_should_end_the_promotion_if_its_been_active_for_longer_than_30_days_and_we_set_a_new_price(self):
        self.subject.set_reduced_price(90)
        self.subject._promotion_started_on = self.subject._promotion_started_on - timedelta(days=31)
        self.subject.set_reduced_price(85)
        self.subject._promotion_active.should.be(False)

    def test_it_should_set_the_promotion_end_date_to_30_days_past_the_start_if_it_expires_in_promotion(self):
        self.subject.set_reduced_price(90)
        self.subject._promotion_started_on = self.subject._promotion_started_on - timedelta(days=31)
        self.subject.in_promotion().should.be(False)
        self.subject._promotion_ended_on.should.equal(self.subject._promotion_started_on + timedelta(days=30))

    def test_it_should_set_the_promotion_end_date_to_30_days_past_the_start_if_it_expires_when_reducing_the_price(self):
        self.subject.set_reduced_price(90)
        self.subject._promotion_started_on = self.subject._promotion_started_on - timedelta(days=31)
        self.subject.set_reduced_price(85)
        self.subject._promotion_active.should.be(False)
        self.subject._promotion_ended_on.should.equal(self.subject._promotion_started_on + timedelta(days=30))

    def test_it_should_end_the_promotion_if_the_price_raises_any_amount(self):
        self.subject.set_reduced_price(90)
        self.subject.in_promotion().should.be(True) #Sanity Check
        self.subject.set_reduced_price(95)
        self.subject.in_promotion().should.be(False)

    def test_it_should_end_the_promotion_if_the_reduced_price_drops_below_30_percent(self):
        self.subject.set_reduced_price(95)
        self.subject.in_promotion().should.be(True) #Santiy Check
        self.subject.set_reduced_price(70)
        self.subject.in_promotion().should.be(True) #Santiy Boundary Check
        self.subject.set_reduced_price(69)
        self.subject.in_promotion().should.be(False)



class TestInventoryItemPromotionComplexCases(unittest.TestCase):
    def setUp(self):
        self.last_price_changed_on = datetime.now() - timedelta(days=30)
        self.subject = InventoryItem(100, self.last_price_changed_on)

    def test_it_should_start_a_promotion_based_on_overall_difference_of_the_original(self):
        self.subject.set_reduced_price(97)
        self.subject.in_promotion().should.be(False)
        self.subject._last_price_changed_on = datetime.now() - timedelta(days=30)
        self.subject.set_reduced_price(95)
        self.subject.in_promotion().should.be(True)

    def test_it_should_start_a_promotion_based_on_overall_diff_of_orig_even_if_reduced_by_less_than_5_percent_this_time(self):
        self.subject.set_reduced_price(95)
        self.subject.in_promotion().should.be(True)
        self.subject.set_reduced_price(96)
        self.subject.in_promotion().should.be(False)
        self.subject._last_price_changed_on = datetime.now() - timedelta(days=30)
        self.subject._promotion_ended_on = datetime.now() - timedelta(days=61)
        self.subject.set_reduced_price(94)
        self.subject.in_promotion().should.be(True)

    def test_it_shouldnt_start_a_promotion_if_promotion_overlaps_30_days_price_stability(self):
        self.subject.set_reduced_price(95)
        self.subject.in_promotion().should.be(True)
        self.subject.set_reduced_price(96)
        self.subject.in_promotion().should.be(False)
        self.subject._promotion_ended_on = datetime.now() - timedelta(days=30)
        self.subject.set_reduced_price(90)
        self.subject.in_promotion().should.be(False)

    def test_it_should_start_a_promotion_if_promotion_period_doesnt_overlap_30_days_price_stability(self):
        self.subject.set_reduced_price(95)
        self.subject.in_promotion().should.be(True)
        self.subject.set_reduced_price(96)
        self.subject.in_promotion().should.be(False)
        self.subject._last_price_changed_on = datetime.now() - timedelta(days=30)
        self.subject._promotion_ended_on = datetime.now() - timedelta(days=61)
        self.subject.set_reduced_price(90)
        self.subject.in_promotion().should.be(True)
