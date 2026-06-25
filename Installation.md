# Full-Stack Unit & Currency Converter App

A small full-stack app for converting currency and common units. It includes a Python Flask backend with a browser-based frontend UI.

## Run locally

1. Create a virtual environment:

    ```powershell
    python -m venv venv
    ```

2. Install dependencies:

    ```powershell
    pip install -r requirements.txt
    ```

3. Start the app:

    ```powershell
    python app.py
    ```

4. Open [http://localhost:5000](http://localhost:5000) in your browser.

## API Endpoints

- `GET /api/rates` returns supported currencies and units.
- `POST /api/convert-currency` converts amount between currencies.
- `POST /api/convert-unit` converts values between supported units.

## Tests

```powershell
pytest
```
