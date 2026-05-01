import streamlit as st
import pandas as pd
import random
import time

st.set_page_config(page_title="Smart Food Rescue", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #e65100;
}
.card {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    margin-bottom: 10px;
}
.highlight {
    background-color: #e8f5e9;
    padding: 20px;
    border-radius: 12px;
    border: 2px solid #2e7d32;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🍽️ Smart Food Rescue System</div>', unsafe_allow_html=True)
st.markdown("---")

# ---------------- SESSION STATE ----------------
if "food_data" not in st.session_state:
    st.session_state.food_data = []

if "meals_delivered" not in st.session_state:
    st.session_state.meals_delivered = 0

# ---------------- DONOR INPUT ----------------
st.subheader("🏪 Donor: Add Surplus Food")

col1, col2, col3 = st.columns(3)

with col1:
    food_name = st.text_input("Food Type")

with col2:
    quantity = st.number_input("Quantity", min_value=1)

with col3:
    expiry = st.slider("Expiry (hours)", 1, 24)

distance = st.slider("Distance to NGO (km)", 1, 20)

if st.button("➕ Add Food Listing"):
    st.session_state.food_data.append({
        "Food": food_name,
        "Quantity": quantity,
        "Expiry": expiry,
        "Distance": distance
    })
    st.success("Food Added Successfully!")

# ---------------- VIEW FOOD ----------------
st.subheader("📦 Available Food")

df = pd.DataFrame(st.session_state.food_data)

if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("No food available yet")

st.markdown("---")

# ---------------- MATCHING ENGINE ----------------
st.subheader("🤖 Intelligent Matching Engine")

if st.button("🔍 Run Matching Engine") and not df.empty:

    # Step 1: Calculate remaining shelf life
    df["Urgency"] = df["Expiry"].apply(lambda x: "High" if x <= 3 else "Normal")

    # Step 2: Priority score (expiry + distance)
    df["Score"] = (1 / df["Expiry"]) + (1 / df["Distance"])

    best = df.sort_values(by="Score", ascending=False).iloc[0]

    st.markdown(f"""
    <div class="highlight">
    <h3>✅ Best Match Found</h3>
    <p><b>Food:</b> {best['Food']}</p>
    <p><b>Quantity:</b> {best['Quantity']}</p>
    <p><b>Urgency:</b> {best['Urgency']}</p>
    <p><b>Reason:</b> Expiry-aware + nearest match</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ---------------- ROUTE SIMULATION ----------------
    st.subheader("🚚 Delivery Simulation")

    st.write("Assigning route to volunteer...")

    progress = st.progress(0)

    for i in range(100):
        time.sleep(0.01)
        progress.progress(i + 1)

    st.success("🚚 Delivery Completed!")

    # ---------------- DYNAMIC REALLOCATION ----------------
    st.subheader("🔄 Dynamic Allocation Check")

    change = random.choice([True, False])

    if change:
        st.warning("⚠️ Demand Center Changed! Redirecting...")
        st.success("➡️ Redirected to secondary center")
    else:
        st.success("✅ Continued to original destination")

    # ---------------- IMPACT ANALYTICS ----------------
    st.subheader("📊 Impact Analytics")

    st.session_state.meals_delivered += int(best["Quantity"])

    co2_saved = st.session_state.meals_delivered * 0.5  # simple estimate

    col1, col2 = st.columns(2)

    with col1:
        st.metric("🍽️ Meals Delivered", st.session_state.meals_delivered)

    with col2:
        st.metric("🌱 CO₂ Saved (kg)", round(co2_saved, 2))

else:
    st.info("Run matching to see intelligent routing")
