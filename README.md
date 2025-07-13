# BSM Pricer

A simple Python module implementing the Black‑Scholes‑Merton (BSM) pricing model for European options, along with a Newton–Raphson solver to compute implied volatility from market prices.

Features

European Call & Put Pricing: Calculates fair option prices under the BSM framework.

Implied Volatility: Uses Newton–Raphson iteration to back out the volatility implied by a given market price.

Easy Integration: Pure Python with minimal dependencies (numpy, scipy).

Requirements

Python 3.7+

NumPy

SciPy

Install via pip:

pip install numpy scipy

Installation

Clone this repository and navigate into its folder:

git clone https://github.com/yourusername/bsm-pricer.git
cd bsm-pricer

Usage

Import the module and call the functions:

from bsm_pricer import bsm_price, implied_vol

# Parameters\ S = 100            # Spot price
K = 100            # Strike price
r = 0.01           # Risk-free rate (continuous)
q = 0.0            # Dividend yield (continuous)
sigma = 0.2       # Volatility
T = 1.0            # Time to maturity (years)

# Price a call
call_price = bsm_price(S, K, r, q, sigma, T, option_type="call")
print(f"Call Price: {call_price:.4f}")

# Solve implied vol from a market price
target_price = 10.5
implied_sigma = implied_vol(S, K, r, q, T, target_price, option_type="call")
print(f"Implied Volatility: {implied_sigma:.4f}")

API Reference

d1(S, K, r, q, sigma, T)

Compute the  term in the BSM formula.

d2(S, K, r, q, sigma, T)

Compute the  term.

bsm_price(S, K, r, q, sigma, T, option_type="call")

Return Black‑Scholes price for a European call or put.

implied_vol(S, K, r, q, T, market_price, option_type="call", initial_guess=0.2, tol=1e-6, max_iter=100)

Solve for implied volatility given a market price.

Testing

You can write simple pytest tests comparing against known analytic or library values. For example:

import pytest
from bsm_pricer import bsm_price

def test_deep_ITM_call():
    price = bsm_price(S=150, K=100, r=0.01, q=0.0, sigma=0.2, T=0.5, option_type="call")
    assert price > 50

Contributing

Feel free to fork, file issues, or submit pull requests.
