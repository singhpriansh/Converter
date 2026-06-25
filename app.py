from flask import Flask, jsonify, request
from converters import currency_convert, unit_convert, CURRENCY_RATES, UNIT_CATEGORIES

app = Flask(__name__, static_folder="static", static_url_path="")

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/api/rates")
def rates():
    return jsonify({
        "currencies": list(CURRENCY_RATES.keys()),
        "units": {category: list(units.keys()) for category, units in UNIT_CATEGORIES.items()}
    })

@app.route("/api/convert-currency", methods=["POST"])
def convert_currency():
    data = request.get_json() or {}
    from_currency = data.get("from_currency")
    to_currency = data.get("to_currency")
    amount = data.get("amount")

    try:
        result = currency_convert(from_currency, to_currency, amount)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    return jsonify({
        "from_currency": from_currency,
        "to_currency": to_currency,
        "amount": amount,
        "converted": round(result, 4)
    })

@app.route("/api/convert-unit", methods=["POST"])
def convert_unit():
    data = request.get_json() or {}
    category = data.get("category")
    from_unit = data.get("from_unit")
    to_unit = data.get("to_unit")
    value = data.get("value")

    try:
        result = unit_convert(category, from_unit, to_unit, value)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    return jsonify({
        "category": category,
        "from_unit": from_unit,
        "to_unit": to_unit,
        "value": value,
        "converted": round(result, 4)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
