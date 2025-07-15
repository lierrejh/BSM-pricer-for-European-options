import numpy as np
from scipy.stats import norm
import yfinance as yf

S = yf.Ticker('AAPL').history(period='1d')['Close'].iloc[-1]


# C = SN (d1) - K e ^ (-rt) N (d2)

# d1 = ln(^s)
# C = Call option price
# S = Current underlying price
# K = Strike Price
# r = Risk-free interest rate
# t = Time to maturity
# N = A normal  distribution

def d1(S,K,r,sigma, t):
    return (np.log(S / K) + (r + ((sigma**2)/2)) * t) / sigma * np.sqrt(t)

def d2(d1, sigma, t):
    return d1 - (sigma * np.sqrt(t))

def BSM_price(d1, d2, S, K, r, t):
    return S * norm(d1) - K * np.exp(-r*t) * norm(d2)