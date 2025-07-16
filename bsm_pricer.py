import numpy as np
from scipy.stats import norm
import yfinance as yf

# C = SN (d1) - K e ^ (-rt) N (d2)

# d1 = ln(^s)
# C = Call option price
# S = Current underlying price
# K = Strike Price
# r = Risk-free interest rate
# t = Time to maturity
# N = A normal  distribution
# q = continuous dividend yield (%pa) - In the original Black-Scholes model, which doesn't account for dividends, the equations are the same as above except: There is just S in place of Se^-qt
# Therefore, if dividend yield is zero, then e-qt = 1 and the models are identical.


def d1(S,K,r,q,sigma, t):
    return (np.log(S / K) + (r - q + ((sigma**2)/2)) * t) / sigma * np.sqrt(t)

def d2(d1, sigma, t):
    return d1 - (sigma * np.sqrt(t))

def BSM_price(d1, d2, S, K, r, t, q, option_type):
    if option_type == 'call':
        return S * np.exp(-q*t) * norm.cdf(d1) - K * np.exp(-r*t) * norm.cdf(d2)
    elif option_type == 'put':
        return K * np.exp(-r*t) * norm.cdf(-d2) - S * np.exp(-q*t) * norm.cdf(-d1)

def get_spot_price():
    import yfinance as yf
    # return yf.Ticker(ticker).history(period='1d')['Close'].iloc[-1]
    return yf.Ticker('MSFT').history(period='1d')['Close'].iloc[-1]

def get_vega(S, K, r, q, sigma, t):
    D1 = d1(S, K, r, q, sigma, t)
    return S * np.exp(-q * t) * norm.pdf(D1) * np.sqrt(t)

def implied_volatility(S, K, r, q, t, market_price, option_type, initial_guess=0.2, tol=1e-5, max_iterations=100):
    sigma = initial_guess
    
    # Newton-Raphson method to find implied volatility

    for i in range(max_iterations):

        # Model price using current sigma

        d1_val = d1(S, K, r, q, sigma, t)
        d2_val = d2(d1_val, sigma, t)
        price = BSM_price(d1_val, d2_val, S, K, r, t, q, option_type)
        
        # Analyse how far off the model price is from the market price 

        price_diff = price - market_price
        
        if abs(price_diff) < tol:
            return sigma
        
       #  Calculate Vega
        vega = get_vega(S, K, r, q, sigma, t)
        if vega < 1e-8:
            raise ValueError("Vega is too small, cannot compute implied volatility.")
        
        # Update sigma using Newton-Raphson formula
        sigma -= price_diff / vega
    
if __name__ == "__main__":
    # Example parameters
    S = get_spot_price() 
    K = 600 
    r = 0.05
    q = 0.02
    t = 1 
    market_price = 100  
    option_type = 'call'

    implied_vol = implied_volatility(S, K, r, q, t, market_price, option_type)
    print(f"Implied Volatility: {implied_vol:.4f}")

    BSM_price_val = BSM_price(d1(S, K, r, q, implied_vol, t), d2(d1(S, K, r, q, implied_vol, t), implied_vol, t), S, K, r, t, q, option_type)
    print(f"Black-Scholes-Merton Price: {BSM_price_val:.2f}")