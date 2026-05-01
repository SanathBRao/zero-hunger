import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random

st.set_page_config(layout="wide")

# ---------------- CSS (IMPORTANT FOR UI) ----------------
st.markdown("""
<style>
/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(#0f3d2e, #1b5e20);
    color: white;
}

/* Cards */
.card {
    background: white;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.08);
}

/* Titles */
h1, h2, h3 {
    color: #1b5e20;
}

/* Section */
.section {
    background: white;
    padding: 15px;
    border-radius: 14px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# ---------------- ROLE SELECT ----------------
st.sidebar.title("🍃 AI FOOD SYSTEM")
role = st.sidebar.selectbox("Select Role", ["Admin", "Donor (Hotel)", "NGO"])

# =====================================================
# 🟢 ADMIN DASHBOARD
# =====================================================
if role == "Admin":

    st.title("📊 Dashboard")
    st.caption("Optimize surplus food allocation and minimize waste")

    # KPI CARDS
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Meals Saved", "12,540", "+18%")
    col2.metric("Food Distributed", "8,320 kg", "+12%")
    col3.metric("Donors", "86", "+5")
    col4.metric("NGOs", "42", "+3")

    st.markdown("---")

    # MAP + TABLE
    col1, col2 = st.columns([2,1])

    with col1:
        st.markdown("### 📍 Live Map - Active Routes")
        st.map(pd.DataFrame({
            'lat': [12.97, 12.98, 12.96],
            'lon': [77.59, 77.60, 77.58]
        }))

    with col2:
        st.markdown("### 📋 Pending Allocations")

        df = pd.DataFrame({
            "Food": ["Meals", "Fruits", "Veg"],
            "Qty": [120, 80, 150],
            "Expiry": ["2 hrs", "5 hrs", "10 hrs"],
            "Priority": ["High", "Medium", "Low"]
        })
        st.dataframe(df)

    st.markdown("---")

    # CHARTS
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Expiry Status")
        fig, ax = plt.subplots()
        ax.pie([30,30,25,15], labels=["High","Med","Low","Safe"], autopct='%1.1f%%')
        st.pyplot(fig)

    with col2:
        st.markdown("### Meals Trend")
        fig, ax = plt.subplots()
        ax.plot([1,2,3,4,5], [2000,4000,6000,7500,9000])
        st.pyplot(fig)

    with col3:
        st.markdown("### Impact")
        st.metric("Meals Saved", "250,400")
        st.metric("CO2 Saved", "18,540 kg")
        st.metric("Money Saved", "₹6,75,000")

    st.success("120 meals allocated to NGO (2 mins ago)")

# =====================================================
# 🏨 DONOR DASHBOARD
# =====================================================
elif role == "Donor (Hotel)":

    st.title("🏨 Donor Dashboard")

    # ADD FOOD
    st.markdown("### ➕ Add Food Listing")

    col1, col2, col3 = st.columns(3)

    food = col1.selectbox("Food Type", ["Rice","Bread","Veg","Fruits"])
    qty = col2.number_input("Quantity", 10)
    expiry = col3.slider("Expiry (hrs)", 1, 24)

    if st.button("Add Food"):
        st.success("Food Listing Added!")

    st.markdown("---")

    # DONATIONS TABLE
    st.markdown("### 📦 Your Donations")

    df = pd.DataFrame({
        "Food": ["Rice","Bread","Veg"],
        "Qty": [100,80,120],
        "Status": ["Pending","Picked","Delivered"]
    })

    st.dataframe(df)

    st.markdown("---")

    # IMPACT
    col1, col2 = st.columns(2)
    col1.metric("Meals Donated", "2,340")
    col2.metric("Waste Reduced", "1,200 kg")

# =====================================================
# 🏢 NGO DASHBOARD
# =====================================================
elif role == "NGO":

    st.title("🏢 NGO Dashboard")

    # AVAILABLE FOOD
    st.markdown("### 🍱 Available Food")

    df = pd.DataFrame({
        "Food": ["Rice","Bread","Fruits"],
        "Qty": [120,80,60],
        "Expiry": [2,5,10],
        "Distance": [3,6,8]
    })

    st.dataframe(df)

    st.markdown("---")

    # MATCHING
    st.markdown("### 🤖 Smart Allocation")

    if st.button("Find Best Match"):

        df["Score"] = (1/df["Expiry"]) + (1/df["Distance"])
        best = df.sort_values(by="Score", ascending=False).iloc[0]

        st.success(f"""
        Best Match → {best['Food']}
        Quantity: {best['Qty']}
        Reason: Closest + Expiry Priority
        """)

    st.markdown("---")

    # DELIVERY
    st.markdown("### 🚚 Active Deliveries")

    delivery = pd.DataFrame({
        "Food": ["Rice","Bread"],
        "Status": ["In Transit","Arriving"],
        "ETA": ["15 mins","30 mins"]
    })

    st.dataframe(delivery)

    st.markdown("---")

    col1, col2 = st.columns(2)
    col1.metric("Meals Received", "5,600")
    col2.metric("People Served", "3,200")
