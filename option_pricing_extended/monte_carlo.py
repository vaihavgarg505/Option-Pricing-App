import numpy as np

def monte_carlo_price(S, K, T, r, sigma, simulations=10000, option_type='call'):
    Z = np.random.standard_normal(simulations)
    ST = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)

    if option_type == 'call':
        payoffs = np.maximum(ST - K, 0)
    else:
        payoffs = np.maximum(K - ST, 0)

    return np.exp(-r * T) * np.mean(payoffs)