import streamlit as st
import pandas as pd
import random

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Zero Hunger System", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background: linear-gradient(to right, #fff3e0, #ffffff);
}
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #e65100;
}
.subtitle {
    text-align: center;
    color: grey;
    margin-bottom: 20px;
}
.card {
    background-color: white;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 10px;
}
.highlight {
    background-color: #e8f5e9;
    padding: 20px;
    border-radius: 15px;
    border: 2px solid #2e7d32;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="title">🍽️ Zero Hunger - Food Redistribution</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Smart Matching of Surplus Food to NGOs</div>', unsafe_allow_html=True)

st.markdown("---")

# ---------------- SIMULATED DATA ----------------
restaurants = ["Hotel A", "Cafe B", "Restaurant C", "Bakery D"]
foods = ["Rice", "Bread", "Veg Curry", "Fruits"]

data = []

for i in range(4):
    data.append({
        "Restaurant": restaurants[i],
        "Food": foods[i],
        "Quantity": random.randint(10, 50),
        "Expiry (hrs)": random.randint(1, 10),
        "Distance (km)": random.randint(1, 15)
    })

df = pd.DataFrame(data)

# ---------------- DISPLAY FOOD ----------------
st.subheader("🍱 Available Surplus Food")

col1, col2 = st.columns(2)

for i, row in df.iterrows():
    with col1 if i % 2 == 0 else col2:
        st.markdown(f"""
        <div class="card">
        <h4>{row['Restaurant']}</h4>
        <p>🍲 Food: {row['Food']}</p>
        <p>📦 Quantity: {row['Quantity']}</p>
        <p>⏳ Expiry: {row['Expiry (hrs)']} hrs</p>
        <p>📍 Distance: {row['Distance (km)']} km</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ---------------- MATCHING LOGIC ----------------
st.subheader("🤖 Smart Matching System")

if st.button("🔍 Find Best Match for NGO"):
    
    # Priority score: lower expiry + lower distance = better
    df["Score"] = (1 / df["Expiry (hrs)"]) + (1 / df["Distance (km)"])
    
    best = df.sort_values(by="Score", ascending=False).iloc[0]

    st.markdown(f"""
    <div class="highlight">
    <h3>✅ Best Match Found</h3>
    <p><b>Restaurant:</b> {best['Restaurant']}</p>
    <p><b>Food:</b> {best['Food']}</p>
    <p><b>Quantity:</b> {best['Quantity']}</p>
    <p><b>Reason:</b> Closest location + earliest expiry</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------------- KPI SECTION ----------------
total_food = df["Quantity"].sum()

col1, col2 = st.columns(2)

with col1:
    st.metric("🍽️ Total Food Available", f"{total_food} meals")

with col2:
    st.metric("🏢 Active Restaurants", len(df))
