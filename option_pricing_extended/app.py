import streamlit as st
from black_scholes import black_scholes_price
from binomial_tree import binomial_tree_price
from monte_carlo import monte_carlo_price
from greeks import black_scholes_greeks
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.set_page_config(page_title="Option Pricing Models", layout="centered")
st.title("📈 Option Pricing Models")
st.markdown("Compare **Black-Scholes**, **Binomial Tree**, and **Monte Carlo** models.")

S = st.number_input("Spot Price (S)", value=100.0)
K = st.number_input("Strike Price (K)", value=100.0)
T = st.number_input("Time to Maturity (T, in years)", value=1.0)
r = st.number_input("Risk-Free Rate (r)", value=0.05)
sigma = st.number_input("Volatility (σ)", value=0.2)
option_type = st.selectbox("Option Type", ['call', 'put'])
american_flag = st.checkbox("Use American Option (Binomial Tree only)", value=False)

if st.button("Calculate Option Prices"):
    bs = black_scholes_price(S, K, T, r, sigma, option_type)
    bt = binomial_tree_price(S, K, T, r, sigma, steps=100, option_type=option_type, american=american_flag)
    mc = monte_carlo_price(S, K, T, r, sigma, simulations=10000, option_type=option_type)

    st.subheader("💰 Option Prices")
    st.write(f"**Black-Scholes Price**: ${bs:.2f}")
    st.write(f"**Binomial Tree Price**: ${bt:.2f}")
    st.write(f"**Monte Carlo Price**: ${mc:.2f}")

    fig, ax = plt.subplots()
    models = ['Black-Scholes', 'Binomial Tree', 'Monte Carlo']
    prices = [bs, bt, mc]
    ax.bar(models, prices, color=['skyblue', 'orange', 'green'])
    ax.set_ylabel('Price')
    ax.set_title(f'{option_type.capitalize()} Option Price Comparison')
    st.pyplot(fig)

    st.subheader("📐 Option Greeks (Black-Scholes)")
    greeks = black_scholes_greeks(S, K, T, r, sigma, option_type)
    for g, val in greeks.items():
        st.write(f"**{g}:** {val:.4f}")

    if option_type == 'call':
        call_price = bs
        put_price = black_scholes_price(S, K, T, r, sigma, 'put')
    else:
        put_price = bs
        call_price = black_scholes_price(S, K, T, r, sigma, 'call')

    lhs = call_price - put_price
    rhs = S - K * np.exp(-r * T)
    parity_diff = abs(lhs - rhs)

    st.subheader("💡 Put-Call Parity Check")
    st.write(f"Call - Put = {lhs:.4f}")
    st.write(f"S - K * exp(-rT) = {rhs:.4f}")
    if parity_diff < 0.1:
        st.success("✅ Put-Call Parity holds (within tolerance)")
    else:
        st.error(f"❌ Put-Call Parity does NOT hold (Δ = {parity_diff:.4f})")

# ------------------- Additional Visualizations -------------------
st.subheader("📊 Option Price vs Strike Price and Time to Maturity")

selected_plot_type = st.selectbox("Choose Option Type for Plots", ["call", "put"])

# Option Price vs Strike Price
Ks = np.linspace(80, 120, 50)
prices_vs_k = [black_scholes_price(S, k, T, r, sigma, selected_plot_type) for k in Ks]
fig1, ax1 = plt.subplots()
ax1.plot(Ks, prices_vs_k)
ax1.set_xlabel("Strike Price (K)")
ax1.set_ylabel("Option Price")
ax1.set_title(f"{selected_plot_type.capitalize()} Option Price vs Strike Price")
st.pyplot(fig1)

# Option Price vs Time to Maturity
Ts = np.linspace(0.1, 2, 50)
prices_vs_t = [black_scholes_price(S, K, t, r, sigma, selected_plot_type) for t in Ts]
fig2, ax2 = plt.subplots()
ax2.plot(Ts, prices_vs_t, color='purple')
ax2.set_xlabel("Time to Maturity (T)")
ax2.set_ylabel("Option Price")
ax2.set_title(f"{selected_plot_type.capitalize()} Option Price vs Time to Maturity")
st.pyplot(fig2)

