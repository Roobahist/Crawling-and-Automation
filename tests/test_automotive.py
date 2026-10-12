"""Offline regression tests for the maintained automotive code."""

import io
import unittest

from crawling_automation.automotive.bama import (
    PriceListFormatError,
    collect_bama_prices,
    parse_bama_prices,
    write_prices,
)
from crawling_automation.automotive.pricing import (
    MileageRule,
    damage_adjusted_price,
    format_price,
    load_damage_coefficients,
    mileage_adjusted_price,
    price_bounds,
    round_price,
)


SAMPLE_LISTING = """
<div class="sefr-price-list"><section>
  <div class="price-list-brand-name"><a>قیمت خودرو پژو</a></div>
  <ul><li>
    <span>206</span><small>1399</small>
    <small class="sefr-company">ایران خودرو</small>
    <small class="sefr-bazaar">نمایندگی</small>
    <small class="sefr-price">123,450,000 تومان</small>
    <small class="sefr-updown price-down">1%</small>
  </li></ul>
</section></div>
"""


class FakeResponse:
    text = SAMPLE_LISTING

    def raise_for_status(self):
        return None


class FakeSession:
    def __init__(self):
        self.last_request = None

    def get(self, url, timeout):
        self.last_request = (url, timeout)
        return FakeResponse()


class PriceTests(unittest.TestCase):
    def test_round_price_ties_down_and_handles_small_amounts(self):
        self.assertEqual(round_price(1_250_000), 1_200_000)
        self.assertEqual(round_price(1_250_001), 1_300_000)
        self.assertEqual(round_price(50_000), 0)
        with self.assertRaises(ValueError):
            round_price(-1)

    def test_boundary_values_receive_nonzero_allowance(self):
        self.assertEqual(price_bounds(25_000_000, 20_000_000), (21_000_000, 19_000_000))
        self.assertEqual(price_bounds(25_000_001, 20_000_000), (22_000_000, 18_000_000))

    def test_damage_coefficients_preserve_application_order(self):
        factors = load_damage_coefficients(io.StringIO("1$2\n0.9$0.8\n"))
        self.assertEqual(damage_adjusted_price(1_000_000, [1, 2], factors), 700_000)
        self.assertEqual(format_price(700_000), "700,000")
        with self.assertRaises(KeyError):
            damage_adjusted_price(1_000_000, [3], factors)
        with self.assertRaises(ValueError):
            load_damage_coefficients(io.StringIO("1$2\n0.9\n"))

    def test_mileage_rules_are_injected(self):
        rule = MileageRule(1.055, 500, 20_000, 60_000, 0.9193)
        self.assertEqual(mileage_adjusted_price(1397, 47_000_000, 20_000, {1397: rule}), 47_000_000)
        self.assertLess(mileage_adjusted_price(1397, 47_000_000, 40_000, {1397: rule}), 47_000_000)
        self.assertGreater(mileage_adjusted_price(1397, 47_000_000, 11_000, {1397: rule}), 47_000_000)

    def test_bama_parser_preserves_price_and_records_dealership(self):
        records = parse_bama_prices(SAMPLE_LISTING, {"پژو": "peugeot"})
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].price_toman, 123_450_000)
        self.assertEqual(records[0].english_brand, "peugeot")
        self.assertEqual(records[0].change, "-1%")
        self.assertTrue(records[0].dealership)
        output = io.StringIO()
        write_prices(records, output)
        self.assertIn("123,450,000 تومان", output.getvalue())

    def test_bama_fetch_is_injected_and_bounded_by_timeout(self):
        session = FakeSession()
        records = collect_bama_prices(session, "https://example.org/list", 6)
        self.assertEqual(len(records), 1)
        self.assertEqual(session.last_request, ("https://example.org/list", 6))

    def test_changed_site_layout_is_not_silently_ignored(self):
        with self.assertRaises(PriceListFormatError):
            parse_bama_prices("<html><body>no list</body></html>")


if __name__ == "__main__":
    unittest.main()
