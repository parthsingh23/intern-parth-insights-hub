from datetime import date

from backend.warmup.utils import fiscal_year, format_inr, parse_pack_size


def test_fiscal_year_before_april():
    assert fiscal_year(date(2026, 3, 31)) == "FY2025-26"


def test_fiscal_year_on_april():
    assert fiscal_year(date(2026, 4, 1)) == "FY2026-27"


def test_fiscal_year_after_april():
    assert fiscal_year(date(2026, 7, 15)) == "FY2026-27"


def test_format_int_large_ammount():
    assert format_inr(60984552.24) == "6,09,84,552.24"


def test_format_int_lakh():
    assert format_inr(100000) == "1,00,000.00"


def test_format_int_small_ammount():
    assert format_inr(500) == "500.00"


def test_parse_pack_size_millilitres():
    assert parse_pack_size("200 ml") == (200, "ml")


def test_parse_pack_size_kilograms():
    assert parse_pack_size("1 kg") == (1, "kg")


def test_parse_pack_size_grams():
    assert parse_pack_size("500 g") == (500, "g")
