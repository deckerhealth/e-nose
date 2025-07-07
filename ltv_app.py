import streamlit as st
import matplotlib.pyplot as plt

# Function to calculate LTV
def calculate_ltv(upfront_price, monthly_fee, annual_fee_growth, churn_rate, discount_rate,
                  annual_addon, addon_growth, years):

    ltv = upfront_price
    active_rate = 1.0

    cash_flows = []

    for t in range(1, years + 1):
        annual_sub_fee = monthly_fee * 12 * ((1 + annual_fee_growth) ** (t - 1))
        annual_addon_revenue = annual_addon * ((1 + addon_growth) ** (t - 1))
        active_rate = active_rate * (1 - churn_rate)
        cash_flow = (annual_sub_fee + annual_addon_revenue) * active_rate
        discount_factor = 1 / ((1 + discount_rate) ** t)
        pv = cash_flow * discount_factor
        ltv += pv
        cash_flows.append(ltv)

    return cash_flows, ltv

# Streamlit interface
st.title("Customer Lifetime Value (LTV) Calculator 💰")

st.sidebar.header("Input Parameters")

upfront_price = st.sidebar.number_input("Upfront product price ($)", 0, 5000, 300)
monthly_fee = st.sidebar.number_input("Monthly subscription fee ($)", 0, 500, 30)
annual_fee_growth = st.sidebar.slider("Annual subscription fee growth rate (%)", 0, 30, 5) / 100
churn_rate = st.sidebar.slider("Annual churn rate (%)", 0, 50, 10) / 100
discount_rate = st.sidebar.slider("Discount rate (%)", 0, 30, 8) / 100
annual_addon = st.sidebar.number_input("Annual add-on sales ($)", 0, 5000, 100)
addon_growth = st.sidebar.slider("Annual add-on growth rate (%)", 0, 30, 7) / 100
years = st.sidebar.slider("Projection years", 1, 20, 10)

cash_flows, final_ltv = calculate_ltv(
    upfront_price, monthly_fee, annual_fee_growth,
    churn_rate, discount_rate, annual_addon,
    addon_growth, years
)

st.write(f"### Estimated total LTV per customer: **${final_ltv:,.2f}**")

# Plot cumulative LTV
fig, ax = plt.subplots()
ax.plot(range(1, years + 1), cash_flows, marker='o')
ax.set_xlabel("Year")
ax.set_ylabel("Cumulative LTV ($)")
ax.set_title("Cumulative LTV Over Time")
ax.grid(True)
st.pyplot(fig)
