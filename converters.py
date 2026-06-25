CURRENCY_RATES = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.8,
    "JPY": 148.0,
    "CAD": 1.35,
    "AUD": 1.5,
    "INR": 83.0,
    "BRL": 5.0
}

UNIT_CATEGORIES = {
    "length": {
        "meter": 1.0,
        "kilometer": 1000.0,
        "mile": 1609.344,
        "yard": 0.9144,
        "foot": 0.3048,
        "inch": 0.0254
    },
    "weight": {
        "gram": 1.0,
        "kilogram": 1000.0,
        "pound": 453.59237,
        "ounce": 28.3495231
    },
    "volume": {
        "liter": 1.0,
        "milliliter": 0.001,
        "gallon": 3.78541,
        "cup": 0.24
    },
    "temperature": {
        "celsius": "celsius",
        "fahrenheit": "fahrenheit",
        "kelvin": "kelvin"
    }
}


def currency_convert(from_currency, to_currency, amount):
    if from_currency not in CURRENCY_RATES:
        raise ValueError(f"Unsupported from_currency: {from_currency}")
    if to_currency not in CURRENCY_RATES:
        raise ValueError(f"Unsupported to_currency: {to_currency}")
    if amount is None:
        raise ValueError("Amount is required")

    try:
        amount = float(amount)
    except (TypeError, ValueError) as exc:
        raise ValueError("Amount must be a number") from exc

    base_amount = amount / CURRENCY_RATES[from_currency]
    return base_amount * CURRENCY_RATES[to_currency]


def _convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value

    if from_unit == "celsius":
        if to_unit == "fahrenheit":
            return value * 9 / 5 + 32
        if to_unit == "kelvin":
            return value + 273.15
    if from_unit == "fahrenheit":
        if to_unit == "celsius":
            return (value - 32) * 5 / 9
        if to_unit == "kelvin":
            return (value - 32) * 5 / 9 + 273.15
    if from_unit == "kelvin":
        if to_unit == "celsius":
            return value - 273.15
        if to_unit == "fahrenheit":
            return (value - 273.15) * 9 / 5 + 32

    raise ValueError(f"Cannot convert temperature from {from_unit} to {to_unit}")


def unit_convert(category, from_unit, to_unit, value):
    if category not in UNIT_CATEGORIES:
        raise ValueError(f"Unsupported category: {category}")
    if from_unit is None or to_unit is None:
        raise ValueError("Both from_unit and to_unit are required")
    if value is None:
        raise ValueError("Value is required")

    try:
        value = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("Value must be a number") from exc

    if category == "temperature":
        return _convert_temperature(value, from_unit, to_unit)

    units = UNIT_CATEGORIES[category]
    if from_unit not in units:
        raise ValueError(f"Unsupported unit: {from_unit}")
    if to_unit not in units:
        raise ValueError(f"Unsupported unit: {to_unit}")

    value_in_base = value * units[from_unit]
    return value_in_base / units[to_unit]
