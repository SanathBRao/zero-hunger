import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide")

# ================= DB =================
conn = sqlite3.connect("food_system.db", check_same_thread=False)
c = conn.cursor()

# USERS
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    role TEXT
)
""")

# FOOD LISTINGS
c.execute("""
CREATE TABLE IF NOT EXISTS food_listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    donor TEXT,
    event_type TEXT,
    food TEXT,
    qty REAL,
    expiry INTEGER,
    location TEXT,
    created_at TEXT
)
""")

# REQUESTS
c.execute("""
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ngo TEXT,
    food_id INTEGER,
    status TEXT
)
""")

conn.commit()

# ================= SESSION =================
if "user" not in st.session_state:
    st.session_state.user = None
    st.session_state.role = None

# ================= AUTH =================
def signup(u, p, r):
    try:
        c.execute("INSERT INTO users VALUES (?, ?, ?)", (u, p, r))
        conn.commit()
        return True
    except:
        return False

def login(u, p):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
    return c.fetchone()

# ================= LOGIN PAGE =================
if not st.session_state.user:

    st.title("🍃 Food Redistribution System")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login(u, p)
            if user:
                st.session_state.user = user[0]
                st.session_state.role = user[2]
                st.rerun()
            else:
                st.error("Invalid login")

    with tab2:
        u = st.text_input("New Username")
        p = st.text_input("New Password", type="password")
        r = st.selectbox("Role", ["Donor", "NGO"])

        if st.button("Create Account"):
            if signup(u, p, r):
                st.success("Account created")
            else:
                st.error("User exists")

    st.stop()

# ================= SIDEBAR =================
st.sidebar.success(f"{st.session_state.user} ({st.session_state.role})")

if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.session_state.role = None
    st.rerun()

# =====================================================
# 🏨 DONOR DASHBOARD (HOTEL + MARRIAGE HALL)
# =====================================================
if st.session_state.role == "Donor":

    st.title("🏨 Donor Dashboard")

    st.subheader("Add Food (Hotel / Marriage Hall Event)")

    event_type = st.selectbox("Source", ["Hotel", "Marriage Hall", "Event Catering"])
    event_name = st.text_input("Event Name (optional)")
    food = st.text_input("Food Type")
    qty = st.number_input("Quantity (kg)", 1)
    expiry = st.slider("Expiry (hours)", 1, 12)
    location = st.text_input("Location")

    if st.button("Submit Food"):
        c.execute("""
        INSERT INTO food_listings 
        (donor, event_type, food, qty, expiry, location, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            st.session_state.user,
            event_type,
            food,
            qty,
            expiry,
            location,
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ))
        conn.commit()
        st.success("Food listed successfully!")

    st.markdown("---")

    st.subheader("Your Listings")

    df = pd.read_sql(
        f"SELECT * FROM food_listings WHERE donor='{st.session_state.user}'",
        conn
    )
    st.dataframe(df)

# =====================================================
# 🏢 NGO DASHBOARD
# =====================================================
elif st.session_state.role == "NGO":

    st.title("🏢 NGO Dashboard")

    st.subheader("Available Food Nearby")

    df = pd.read_sql("SELECT * FROM food_listings", conn)

    if not df.empty:
        st.dataframe(df)

        selected_id = st.selectbox("Select Food ID to Request", df["id"])

        if st.button("Request Food"):
            c.execute("""
            INSERT INTO requests (ngo, food_id, status)
            VALUES (?, ?, ?)
            """, (st.session_state.user, selected_id, "Pending"))
            conn.commit()
            st.success("Request sent!")

    else:
        st.info("No food available currently")

    st.markdown("---")

    st.subheader("My Requests")

    req = pd.read_sql(
        f"SELECT * FROM requests WHERE ngo='{st.session_state.user}'",
        conn
    )
    st.dataframe(req)

# =====================================================
# 🟢 ADMIN VIEW (OPTIONAL SIMPLE)
# =====================================================
st.markdown("---")
st.subheader("📊 System Overview")

food_data = pd.read_sql("SELECT * FROM food_listings", conn)
req_data = pd.read_sql("SELECT * FROM requests", conn)

col1, col2 = st.columns(2)
col1.metric("Total Listings", len(food_data))
col2.metric("Total Requests", len(req_data))
