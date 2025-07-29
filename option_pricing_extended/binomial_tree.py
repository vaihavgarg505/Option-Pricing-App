import numpy as np

def binomial_tree_price(S, K, T, r, sigma, steps=100, option_type='call', american=False):
    dt = T / steps
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)

    prices = np.array([S * (u ** j) * (d ** (steps - j)) for j in range(steps + 1)])
    if option_type == 'call':
        values = np.maximum(prices - K, 0)
    else:
        values = np.maximum(K - prices, 0)

    for i in range(steps - 1, -1, -1):
        prices = prices[:i + 1] * u
        values = np.exp(-r * dt) * (p * values[1:i + 2] + (1 - p) * values[0:i + 1])
        if american:
            intrinsic = np.maximum(prices - K, 0) if option_type == 'call' else np.maximum(K - prices, 0)
            values = np.maximum(values, intrinsic)

    return values[0]