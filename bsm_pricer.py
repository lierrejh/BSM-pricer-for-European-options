import numpy as np
from scipy.stats import norm
import yfinance as yf
from datetime import datetime

def d1(S, K, r, q, sigma, t):
    num = np.log(S / K) + (r - q + 0.5 * sigma**2) * t
    den = sigma * np.sqrt(t)
    return num / den

def bsm_price(S, K, r, q, sigma, t, option_type="call"):
    D1 = d1(S, K, r, q, sigma, t)
    D2 = D1 - sigma * np.sqrt(t)
    df_q = np.exp(-q * t)
    df_r = np.exp(-r * t)

    if option_type.lower() in ("call","calls"):
        return df_q * S * norm.cdf(D1) - df_r * K * norm.cdf(D2)
    elif option_type.lower() in ("put","puts"):
        return df_r * K * norm.cdf(-D2) - df_q * S * norm.cdf(-D1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

def vega(S, K, r, q, sigma, t):
    D1 = d1(S, K, r, q, sigma, t)
    return S * np.exp(-q * t) * norm.pdf(D1) * np.sqrt(t)

def implied_volatility(
    S, K, r, q, t, market_price,
    option_type="call",
    initial_guess=0.2,
    tol=1e-6,
    max_iter=100
):
    sigma = initial_guess
    for _ in range(max_iter):
        price = bsm_price(S, K, r, q, sigma, t, option_type)
        diff  = price - market_price
        if abs(diff) < tol:
            return sigma
        vol = vega(S, K, r, q, sigma, t)
        if vol < 1e-8:
            raise RuntimeError("Vega too small")
        sigma -= diff / vol
        sigma = max(sigma, tol)
    raise RuntimeError("IV did not converge")

def find_mispricings(ticker, expiry, sigma_forecast, option_type, abs_thresh=0.5, pct_thresh=2):
    t = yf.Ticker(ticker)
    # 1) Spot & dividend
    hist = t.history(period="1d")
    S    = hist["Close"].iloc[-1]
    q    = t.info.get("dividendYield", 0.0) or 0.0
    r    = 0.04
    # 2) Time‐to‐expiry
    T    = (datetime.strptime(expiry, "%Y-%m-%d").date() - datetime.today().date()).days / 365.0
    # 3) Choose calls or puts
    chain  = t.option_chain(expiry)
    contract = chain.calls if option_type.lower().startswith("call") else chain.puts

    results = []
    for _, row in contract.iterrows():
        K = row.strike
        bid, ask = row.bid, row.ask
        if bid <= 0 or ask <= 0: continue

        C_mkt = (bid + ask) / 2
        
        try:
            sigma_iv = implied_volatility(S, K, r, q, T, C_mkt, option_type)
        except RuntimeError:
            continue

        C_mod = bsm_price(S, K, r, q, sigma_forecast, T, option_type)
        D1 = d1(S, K, r, q, sigma_iv, T)
        if option_type.lower().startswith("call"):
            delta = np.exp(-q*T) * norm.cdf(D1)
        else:
            delta = np.exp(-q*T) * (norm.cdf(D1) - 1)

        pct = (C_mkt - C_mod) / C_mod * 100

        if abs(delta) >= abs_thresh and abs(pct) >= pct_thresh:
            results.append({
                "strike":        K,
                "market_price":  C_mkt,
                "model_price":   C_mod,
                "implied_vol":   sigma_iv,
                "delta":         delta,
            })
    return results

if __name__ == "__main__":
    ticker = "MSFT"
    expiry = yf.Ticker(ticker).options[0]
    mis    = find_mispricings(ticker, expiry, sigma_forecast=0.20, option_type="puts")
    for m in mis:
        print(m)
