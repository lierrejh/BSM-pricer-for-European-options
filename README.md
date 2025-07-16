# Option Mispricing Scanner

A Python script for pricing European options using the Black–Scholes–Merton model, computing implied volatility via Newton–Raphson, and scanning live option chains for mispriced contracts based on absolute and percentage thresholds.

## Features

* **Vanilla BSM Pricer**: `bsm_price` for calls and puts, accounting for dividends.
* **Implied Vol Solver**: `implied_volatility` backs out market-implied σ from live quotes.
* **Greeks**: `vega` and on-the-fly `delta` calculation for filtering.
* **Live Data Integration**: Fetch spot, dividend yield, and option chains via `yfinance`.
* **Mispricing Scan**: `find_mispricings` loops through calls or puts, applies absolute and relative filters, and returns actionable strikes.

## Requirements

* Python 3.7+
* NumPy
* SciPy
* yfinance

Install dependencies:

```bash
pip install numpy scipy yfinance
```

## Installation

Clone or download this script into your project directory:

```bash
git clone https://github.com/lierrejh/option-mispricer.git
cd option-mispricer
```

## Usage

1. **Set parameters** in the `__main__` block at the bottom:

   * `ticker`: e.g. `"MSFT"`
   * `expiry`: first entry from `yf.Ticker(ticker).options`
   * `sigma_forecast`: your forecast vol (e.g. `0.20` for 20%)
   * `option_type`: `"calls"` or `"puts"`
   * `abs_thresh`: minimum \$ price gap (default `0.5`)
   * `pct_thresh`: minimum % gap (default `2`)

2. **Run the script**:

```bash
python option_mispricer.py
```

3. **Interpret output**: Each line is a dict with:

   * `strike`: strike price
   * `market_price`: mid-market premium
   * `model_price`: BSM price at `sigma_forecast`
   * `implied_vol`: solved market-implied volatility
   * `delta`: option delta used for direction/hedge sizing

## API Reference

### `d1(S, K, r, q, sigma, t)`

Compute the BSM intermediate
$d_1 = \frac{\ln(S/K)+(r-q+0.5\sigma^2)t}{\sigma\sqrt{t}}$.

### `bsm_price(S, K, r, q, sigma, t, option_type)`

Return BSM price for European calls/puts.  `option_type` can be `"call"`, `"calls"`, `"put"`, or `"puts"`.

### `vega(S, K, r, q, sigma, t)`

Compute Vega (∂Price/∂σ) = $S e^{-q t} φ(d_1) \sqrt{t}$.

### `implied_volatility(S, K, r, q, t, market_price, option_type, initial_guess, tol, max_iter)`

Newton–Raphson solver to back out implied volatility that matches `market_price`.

### `find_mispricings(ticker, expiry, sigma_forecast, option_type, abs_thresh, pct_thresh)`

Scan live option chain via `yfinance` and return list of dicts for contracts where:

```
|market_price - model_price| >= abs_thresh
and
|(market_price - model_price)/model_price|*100 >= pct_thresh
```

## Example

```python
if __name__ == "__main__":
    ticker = "MSFT"
    expiry = yf.Ticker(ticker).options[0]
    results = find_mispricings(
        ticker,
        expiry,
        sigma_forecast=0.20,
        option_type="puts",
        abs_thresh=0.5,
        pct_thresh=2
    )
    for m in results:
        print(m)
```
