import pytest
from converters import currency_convert, unit_convert


def test_currency_convert_usd_to_eur():
    result = currency_convert("USD", "EUR", 100)
    assert pytest.approx(result, rel=1e-3) == 92.0


def test_currency_convert_invalid_currency():
    with pytest.raises(ValueError, match="Unsupported from_currency"):
        currency_convert("ABC", "USD", 10)


def test_unit_convert_length():
    result = unit_convert("length", "meter", "kilometer", 1500)
    assert pytest.approx(result, rel=1e-3) == 1.5


def test_unit_convert_temperature():
    result = unit_convert("temperature", "celsius", "fahrenheit", 0)
    assert result == 32


def test_unit_convert_invalid_category():
    with pytest.raises(ValueError, match="Unsupported category"):
        unit_convert("speed", "mps", "kph", 10)
