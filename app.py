import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import hashlib

st.set_page_config(layout="wide")

# ================= DATABASE =================
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    role TEXT
)
""")
conn.commit()

# ================= HELPERS =================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password, role):
    try:
        c.execute("INSERT INTO users VALUES (?, ?, ?)",
                  (username, hash_password(password), role))
        conn.commit()
        return True
    except:
        return False

def login_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, hash_password(password)))
    return c.fetchone()

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None

# ================= CSS =================
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background: linear-gradient(#0f3d2e, #1b5e20);
}
h1, h2, h3 {
    color: #1b5e20;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 🔐 AUTH PAGE (LOGIN + SIGNUP)
# =====================================================
if not st.session_state.logged_in:

    st.title("🍃 AI Food Redistribution System")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    # -------- LOGIN --------
    with tab1:
        st.subheader("Login")

        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            user = login_user(username, password)

            if user:
                st.session_state.logged_in = True
                st.session_state.username = user[0]
                st.session_state.role = user[2]
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")

    # -------- SIGNUP --------
    with tab2:
        st.subheader("Create Account")

        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")
        role = st.selectbox("Select Role", ["Admin", "Donor (Hotel)", "NGO"])

        if st.button("Sign Up"):
            if add_user(new_user, new_pass, role):
                st.success("Account created successfully! Please login.")
            else:
                st.error("Username already exists")

    st.stop()

# =====================================================
# 🔄 SIDEBAR
# =====================================================
role = st.session_state.role

st.sidebar.title("🍃 AI FOOD SYSTEM")
st.sidebar.success(f"{st.session_state.username} ({role})")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.rerun()

# =====================================================
# 🟢 ADMIN DASHBOARD
# =====================================================
if role == "Admin":

    st.title("📊 Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Meals Saved", "12,540", "+18%")
    col2.metric("Food Distributed", "8,320 kg", "+12%")
    col3.metric("Donors", "86", "+5")
    col4.metric("NGOs", "42", "+3")

    st.markdown("---")

    col1, col2 = st.columns([2,1])

    with col1:
        st.map(pd.DataFrame({
            'lat': [12.97, 12.98, 12.96],
            'lon': [77.59, 77.60, 77.58]
        }))

    with col2:
        df = pd.DataFrame({
            "Food": ["Meals", "Fruits", "Veg"],
            "Qty": [120, 80, 150],
            "Expiry": ["2 hrs", "5 hrs", "10 hrs"]
        })
        st.dataframe(df)

# =====================================================
# 🏨 DONOR
# =====================================================
elif role == "Donor (Hotel)":

    st.title("🏨 Donor Dashboard")

    food = st.selectbox("Food Type", ["Rice","Bread","Veg","Fruits"])
    qty = st.number_input("Quantity", 10)
    expiry = st.slider("Expiry (hrs)", 1, 24)

    if st.button("Add Food"):
        st.success("Food Added!")

# =====================================================
# 🏢 NGO
# =====================================================
elif role == "NGO":

    st.title("🏢 NGO Dashboard")

    df = pd.DataFrame({
        "Food": ["Rice","Bread","Fruits"],
        "Qty": [120,80,60],
        "Expiry": [2,5,10],
        "Distance": [3,6,8]
    })

    st.dataframe(df)

    if st.button("Find Best Match"):
        df["Score"] = (1/df["Expiry"]) + (1/df["Distance"])
        best = df.sort_values(by="Score", ascending=False).iloc[0]

        st.success(f"Best Match: {best['Food']} ({best['Qty']})")

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
