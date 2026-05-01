import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# ================= SESSION STORAGE =================
if "food" not in st.session_state:
    st.session_state.food = []

if "demand" not in st.session_state:
    st.session_state.demand = []

# ================= TITLE =================
st.title("🍃 Smart Food Redistribution (Concept Demo)")
st.caption("Demonstrates Donor → System → NGO flow with dynamic allocation")

st.markdown("---")

# ================= 3 COLUMNS =================
col1, col2, col3 = st.columns(3)

# =====================================================
# 🏨 DONOR
# =====================================================
with col1:
    st.subheader("🏨 Donor")

    food = st.text_input("Food Type")
    qty = st.number_input("Quantity", 1)
    expiry = st.slider("Expiry (hrs)", 1, 12)

    if st.button("Add Food"):
        st.session_state.food.append({
            "food": food,
            "qty": qty,
            "expiry": expiry
        })
        st.success("Food Added")

    st.write("### Available Food")
    st.dataframe(pd.DataFrame(st.session_state.food))

# =====================================================
# 🧠 SYSTEM (MATCHING ENGINE)
# =====================================================
with col2:
    st.subheader("🤖 Matching Engine")

    if st.button("Run Allocation"):

        results = []

        for d in st.session_state.demand:
            best = None
            best_score = -1

            for f in st.session_state.food:
                score = (1/f["expiry"]) + (f["qty"]/100)

                if score > best_score:
                    best_score = score
                    best = f

            if best:
                results.append({
                    "NGO": d["ngo"],
                    "Food": best["food"],
                    "Qty": best["qty"]
                })

        st.session_state.results = results

    if "results" in st.session_state:
        st.success("Allocation Done")
        st.dataframe(pd.DataFrame(st.session_state.results))

# =====================================================
# 🏢 NGO
# =====================================================
with col3:
    st.subheader("🏢 NGO")

    ngo = st.text_input("NGO Name")
    need = st.number_input("Food Needed", 1)

    if st.button("Request Food"):
        st.session_state.demand.append({
            "ngo": ngo,
            "need": need
        })
        st.success("Request Added")

    st.write("### NGO Demand")
    st.dataframe(pd.DataFrame(st.session_state.demand))

# =====================================================
# FLOW EXPLANATION
# =====================================================
st.markdown("---")
st.subheader("🔁 Flow Explanation")

st.info("""
1. Donor adds surplus food  
2. NGO raises demand  
3. Matching Engine assigns best food  
4. System optimizes based on expiry + quantity  
""")
