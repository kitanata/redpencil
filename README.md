Red Pencil Code Kata
====================

Inspired From: [Stefen Roock](http://stefanroock.wordpress.com/2011/03/04/red-pencil-code-kata/)

1. We provide a shopping portal, where dealers can offer their goods (similiar to Amazon market place). We want to support red pencil promotions for reduced prices. During the red pencil promotion the old price is crossed out in red and the new reduced price is written next to it.
2. To avoid misuse of red pencil promotions the red pencil promotions are activated and deactivated automatically.
3. The scope of the Code Kata is the implementations of the rules for activation and end of red pencil promotions.
4. A red pencil promotion starts due to a price reduction. The price has to be reduced by at least 5% but at most by 30% and the previous price had to be stable for at least 30 days.
5. A red pencil promotion lasts 30 days as the maximum length.
6. If the price is further reduced during the red pencil promotion the promotion will not be prolonged by that reduction.
7. If the price is increased during the red pencil promotion the promotion will be ended immediately.
8. If the price if reduced during the red pencil promotion so that the overall reduction is more than 30% with regard to the original price, the promotion is ended immediately.
9. After a red pencil promotion is ended additional red pencil promotions may follow – as long as the start condition is valid: the price was stable for 30 days and these 30 days don’t intersect with a previous red pencil promotion.

Installation
============

The code is written in Python 3.4.

Install with pip3. `pip3 install -r requirements.txt`
Run the tests. `nosetests`
