import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from math import radians, cos, sin, sqrt, atan2

st.set_page_config(layout="wide")

# ================= DATABASE =================
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

# FOOD
c.execute("""
CREATE TABLE IF NOT EXISTS food_listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    donor TEXT,
    event_type TEXT,
    food TEXT,
    qty REAL,
    expiry INTEGER,
    lat REAL,
    lon REAL,
    assigned_ngo TEXT,
    status TEXT DEFAULT 'Available',
    created_at TEXT
)
""")

# NGO DEMAND
c.execute("""
CREATE TABLE IF NOT EXISTS ngo_demand (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ngo TEXT,
    qty_needed REAL,
    food_pref TEXT,
    lat REAL,
    lon REAL,
    urgency INTEGER,
    status TEXT DEFAULT 'Open',
    created_at TEXT
)
""")

conn.commit()

# ================= HELPERS =================
def distance_km(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2-lat1)
    dlon = radians(lon2-lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    return R * (2 * atan2(sqrt(a), sqrt(1-a)))

def score(d, f, dist):
    return (
        0.4*(1/max(d['urgency'],1)) +
        0.3*(1/max(f['expiry'],1)) +
        0.2*(1/(dist+1)) +
        0.1*(min(f['qty'], d['qty_needed'])/max(d['qty_needed'],1))
    )

def allocate():
    foods = pd.read_sql("SELECT * FROM food_listings WHERE status='Available'", conn)
    demands = pd.read_sql("SELECT * FROM ngo_demand WHERE status='Open'", conn)

    for _, d in demands.iterrows():
        best_id, best_score = None, -1

        for _, f in foods.iterrows():
            if d['food_pref'] and d['food_pref'].lower() not in f['food'].lower():
                continue

            dist = distance_km(d['lat'], d['lon'], f['lat'], f['lon'])
            s = score(d, f, dist)

            if s > best_score:
                best_score = s
                best_id = f['id']

        if best_id:
            c.execute("UPDATE food_listings SET assigned_ngo=?, status='Allocated' WHERE id=?",
                      (d['ngo'], best_id))
            c.execute("UPDATE ngo_demand SET status='Fulfilled' WHERE id=?", (d['id'],))
            conn.commit()

def reallocate():
    df = pd.read_sql("SELECT * FROM food_listings WHERE status='Allocated'", conn)

    for _, f in df.iterrows():
        mins = (pd.Timestamp.now() - pd.to_datetime(f['created_at'])).total_seconds()/60

        if mins > 15 or f['expiry'] <= 2:
            c.execute("UPDATE food_listings SET status='Available', assigned_ngo=NULL WHERE id=?",
                      (f['id'],))
            conn.commit()

    allocate()

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
        r = st.selectbox("Role", ["Donor", "NGO", "Admin"])
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
# 🏨 DONOR
# =====================================================
if st.session_state.role == "Donor":

    st.title("🏨 Donor Dashboard")

    event_type = st.selectbox("Source", ["Hotel", "Marriage Hall"])
    food = st.text_input("Food Type")
    qty = st.number_input("Quantity (kg)", 1)
    expiry = st.slider("Expiry (hours)", 1, 12)

    lat = st.number_input("Latitude", value=12.9716)
    lon = st.number_input("Longitude", value=77.5946)

    if st.button("Submit Food"):
        c.execute("""
        INSERT INTO food_listings 
        (donor, event_type, food, qty, expiry, lat, lon, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (st.session_state.user, event_type, food, qty, expiry, lat, lon,
              datetime.now().strftime("%Y-%m-%d %H:%M")))
        conn.commit()
        st.success("Food added!")

    st.dataframe(pd.read_sql(
        f"SELECT * FROM food_listings WHERE donor='{st.session_state.user}'", conn))

# =====================================================
# 🏢 NGO
# =====================================================
elif st.session_state.role == "NGO":

    st.title("🏢 NGO Dashboard")

    st.subheader("📢 Raise Requirement")

    qty = st.number_input("Quantity Needed", 1)
    pref = st.text_input("Food Preference")
    lat = st.number_input("Latitude", value=12.9716)
    lon = st.number_input("Longitude", value=77.5946)
    urgency = st.slider("Urgency (hrs)", 1, 12)

    if st.button("Submit Requirement"):
        c.execute("""
        INSERT INTO ngo_demand 
        (ngo, qty_needed, food_pref, lat, lon, urgency, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (st.session_state.user, qty, pref, lat, lon, urgency,
              datetime.now().strftime("%Y-%m-%d %H:%M")))
        conn.commit()
        st.success("Request submitted")

    st.subheader("🎯 Assigned Food")

    df = pd.read_sql(f"""
    SELECT * FROM food_listings 
    WHERE assigned_ngo='{st.session_state.user}'
    """, conn)

    st.map(df[["lat","lon"]] if not df.empty else pd.DataFrame())

    st.dataframe(df)

# =====================================================
# 🟢 ADMIN
# =====================================================
elif st.session_state.role == "Admin":

    st.title("🛠️ Admin Dashboard")

    if st.button("Run Allocation"):
        allocate()
        st.success("Allocated")

    if st.button("Run Reallocation"):
        reallocate()
        st.success("Reallocated")

    st.subheader("📦 Food")
    st.dataframe(pd.read_sql("SELECT * FROM food_listings", conn))

    st.subheader("📢 NGO Demand")
    st.dataframe(pd.read_sql("SELECT * FROM ngo_demand", conn))

# =====================================================
# ⚡ AUTO ENGINE
# =====================================================
allocate()
reallocate()
