import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Smart Water System", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background: linear-gradient(to right, #e0f7fa, #ffffff);
}
.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #0077b6;
}
.subtitle {
    text-align: center;
    color: grey;
    margin-bottom: 20px;
}
.card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="title">💧 Smart Water Monitoring System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-Based Leak Detection & Redistribution</div>', unsafe_allow_html=True)

st.markdown("---")

# ---------------- DATA ----------------
zones = ["Zone A", "Zone B", "Zone C", "Zone D", "Zone E"]
usage = [random.randint(80, 200) for _ in zones]

df = pd.DataFrame({
    "Zone": zones,
    "Water Usage (L)": usage
})

avg_usage = df["Water Usage (L)"].mean()

status = []
alerts = 0

for u in usage:
    if u > avg_usage * 1.5:
        status.append("🚨 Leak")
        alerts += 1
    elif u > avg_usage * 1.2:
        status.append("⚠️ High")
        alerts += 1
    else:
        status.append("✅ Normal")

df["Status"] = status

# ---------------- KPI CARDS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f'<div class="card"><h3>Total Usage</h3><h2>{sum(usage)} L</h2></div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<div class="card"><h3>Average Usage</h3><h2>{round(avg_usage,2)} L</h2></div>', unsafe_allow_html=True)

with col3:
    st.markdown(f'<div class="card"><h3>Alerts</h3><h2>{alerts}</h2></div>', unsafe_allow_html=True)

st.markdown("---")

# ---------------- TABLE + CHART ----------------
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📊 Zone Status")
    st.dataframe(df, use_container_width=True)

with col2:
    st.subheader("📈 Usage Chart")
    fig, ax = plt.subplots()
    ax.bar(df["Zone"], df["Water Usage (L)"])
    ax.set_xlabel("Zones")
    ax.set_ylabel("Water Usage (L)")
    ax.set_title("Water Consumption")
    st.pyplot(fig)

st.markdown("---")

# ---------------- REDISTRIBUTION ----------------
st.subheader("🔄 Smart Redistribution Suggestions")

high = df[df["Status"] != "✅ Normal"]
normal = df[df["Status"] == "✅ Normal"]

if not high.empty and not normal.empty:
    for i in range(min(len(high), len(normal))):
        st.success(f"➡️ Redirect water from {normal.iloc[i]['Zone']} to {high.iloc[i]['Zone']}")
else:
    st.info("All zones are balanced. No action needed.")

st.markdown("---")

# ---------------- BUTTON ----------------
if st.button("🔍 Run New Analysis"):
    st.rerun()