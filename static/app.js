const currencyFrom = document.getElementById("currencyFrom");
const currencyTo = document.getElementById("currencyTo");
const currencyAmount = document.getElementById("currencyAmount");
const currencyResult = document.getElementById("currencyResult");
const currencyConvert = document.getElementById("currencyConvert");

const unitCategory = document.getElementById("unitCategory");
const unitValue = document.getElementById("unitValue");
const unitFrom = document.getElementById("unitFrom");
const unitTo = document.getElementById("unitTo");
const unitResult = document.getElementById("unitResult");
const unitConvert = document.getElementById("unitConvert");

let rates = null;

async function fetchRates() {
    const response = await fetch("/api/rates");
    if (!response.ok) {
        throw new Error("Failed to load rates")
    }
    return response.json();
}

function populateCurrencyOptions(currencies) {
    currencyFrom.innerHTML = "";
    currencyTo.innerHTML = "";
    currencies.forEach(code => {
        const option1 = document.createElement("option");
        option1.value = code;
        option1.textContent = code;
        currencyFrom.append(option1);

        const option2 = document.createElement("option");
        option2.value = code;
        option2.textContent = code;
        currencyTo.append(option2);
    });
    currencyFrom.value = "USD";
    currencyTo.value = "EUR";
}

function populateUnitCategories(categories) {
    unitCategory.innerHTML = "";
    Object.keys(categories).forEach(category => {
        const option = document.createElement("option");
        option.value = category;
        option.textContent = category.charAt(0).toUpperCase() + category.slice(1);
        unitCategory.append(option);
    });
}

function populateUnitOptions(category) {
    const units = rates.units[category] || [];
    unitFrom.innerHTML = "";
    unitTo.innerHTML = "";
    units.forEach(unit => {
        const option1 = document.createElement("option");
        option1.value = unit;
        option1.textContent = unit;
        unitFrom.append(option1);

        const option2 = document.createElement("option");
        option2.value = unit;
        option2.textContent = unit;
        unitTo.append(option2);
    });
    unitFrom.value = units[0] || "";
    unitTo.value = units[1] || units[0] || "";
}

function showResult(target, text, isError = false) {
    target.textContent = text;
    target.style.color = isError ? "#b91c1c" : "#111827";
}

async function doCurrencyConvert() {
    try {
        const response = await fetch("/api/convert-currency", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                from_currency: currencyFrom.value,
                to_currency: currencyTo.value,
                amount: currencyAmount.value
            })
        });

        const payload = await response.json();
        if (!response.ok) {
            showResult(currencyResult, payload.error || "Conversion failed", true);
            return;
        }

        showResult(currencyResult, `${payload.amount} ${payload.from_currency} = ${payload.converted} ${payload.to_currency}`);
    } catch (error) {
        showResult(currencyResult, error.message, true);
    }
}

async function doUnitConvert() {
    try {
        const response = await fetch("/api/convert-unit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                category: unitCategory.value,
                from_unit: unitFrom.value,
                to_unit: unitTo.value,
                value: unitValue.value
            })
        });

        const payload = await response.json();
        if (!response.ok) {
            showResult(unitResult, payload.error || "Conversion failed", true);
            return;
        }

        showResult(unitResult, `${payload.value} ${payload.from_unit} = ${payload.converted} ${payload.to_unit}`);
    } catch (error) {
        showResult(unitResult, error.message, true);
    }
}

unitCategory.addEventListener("change", () => {
    populateUnitOptions(unitCategory.value);
});

currencyConvert.addEventListener("click", doCurrencyConvert);
unitConvert.addEventListener("click", doUnitConvert);

(async function init() {
    try {
        rates = await fetchRates();
        populateCurrencyOptions(rates.currencies);
        populateUnitCategories(rates.units);
        populateUnitOptions(unitCategory.value);
    } catch (error) {
        showResult(currencyResult, error.message, true);
        showResult(unitResult, error.message, true);
    }
})();
