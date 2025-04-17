import streamlit as st
import pandas as pd
import uuid

st.set_page_config(page_title="Kennel Suite Builder", layout="wide")
st.title("Kennel Suite Builder")

st.write("""
Use this form to add each type of kennel suite you offer. Fill out the details for each suite, then click 'Add Suite'. All added suites will be shown below as summary cards.
""")

# --- Kennel Suite Entry ---
if "kennel_suites" not in st.session_state:
    st.session_state.kennel_suites = []

with st.form("add_kennel_suite_form"):
    suite_name = st.selectbox(
        "Suite Name",
        [
            "Small",
            "Medium",
            "Large",
            "Jr. Suite",
            "Luxury Suite",
            "Other",
        ],
    )
    col_len, col_wid = st.columns(2)
    with col_len:
        suite_length = st.number_input("Suite Length (ft)", min_value=0, step=1, format="%d")
    with col_wid:
        suite_width = st.number_input("Suite Width (ft)", min_value=0, step=1, format="%d")
    potty_breaks = st.number_input("# of Daily Potty Breaks", min_value=0, step=1)
    accommodates_lbs = st.number_input("Accommodates up to (lbs)", min_value=0, step=1)
    price_per_night = st.number_input("Price per Dog per Night ($)", min_value=0.0, step=1.0)
    price_two_dogs = st.number_input("Price per Night for 2 Dogs ($)", min_value=0.0, step=1.0)
    price_two_dogs_same_kennel = st.number_input("Price per Night for 2 Dogs ($) - Shared Kennel", min_value=0.0, step=1.0)

    features = st.text_area("Bulleted List of Features (one per line)")
    submitted = st.form_submit_button("Add Suite")
    if submitted:
        st.session_state.kennel_suites.append({
            "id": str(uuid.uuid4()),
            "suite_name": suite_name,
            "suite_length": suite_length,
            "suite_width": suite_width,
            "potty_breaks": potty_breaks,
            "accommodates_lbs": accommodates_lbs,
            "price_per_night": price_per_night,
            "price_two_dogs": price_two_dogs,
            "price_two_dogs_same_kennel": price_two_dogs_same_kennel,
            "features": [f.strip() for f in features.split("\n") if f.strip()],
        })
        st.success(f"Added suite: {suite_name}")

# --- Display Suites as Cards ---
if st.session_state.kennel_suites:
    st.subheader("Current Suites")
    for suite in st.session_state.kennel_suites:
        # Single dog card
        st.markdown(f"""
        <div style='background-color:#eaf0fb; border-radius:18px; padding:24px; margin-bottom:18px; box-shadow: 0 2px 8px #00000010;'>
            <h2 style='margin-bottom:4px; color:#2a3e5c;'><span style='font-size:1.3em;'>🏠</span> {suite['suite_name']} (1 Dog)</h2>
            <span style='font-size:2em; color:#fcbf49; font-weight:bold;'>${int(suite['price_per_night'])}</span><span style='color:#fcbf49;'>/night</span><br>
            <ul style='margin:10px 0 6px 0; padding-left:18px;'>
                <li>{suite.get('suite_length', '')}x{suite.get('suite_width', '')} ft Indoor Suite</li>
                <li>{suite['potty_breaks']} Daily Potty Break{'s' if suite['potty_breaks']!=1 else ''}</li>
                <li>Accommodates up to {suite['accommodates_lbs']} lbs</li>
            </ul>
            <ul style='color:#2a3e5c; font-size:1.07em; margin:0 0 0 18px; padding-left:0;'>
                {''.join([f'<li>{f}</li>' for f in suite['features']])}
            </ul>
        </div>
        """, unsafe_allow_html=True)
        # Two dog card for price_two_dogs
        if suite.get('price_two_dogs', 0) > 0:
            st.markdown(f"""
            <div style='background-color:#eaf0fb; border-radius:18px; padding:24px; margin-bottom:18px; box-shadow: 0 2px 8px #00000010;'>
                <h2 style='margin-bottom:4px; color:#2a3e5c;'><span style='font-size:1.3em;'>🏠</span> {suite['suite_name']} (2 Dogs)</h2>
                <span style='font-size:2em; color:#fcbf49; font-weight:bold;'>${int(suite['price_two_dogs'])}</span><span style='color:#fcbf49;'>/night</span><br>
                <ul style='margin:10px 0 6px 0; padding-left:18px;'>
                    <li>{suite.get('suite_length', '')}x{suite.get('suite_width', '')} ft Indoor Suite</li>
                    <li>{suite['potty_breaks']} Daily Potty Break{'s' if suite['potty_breaks']!=1 else ''}</li>
                    <li>Accommodates up to {suite['accommodates_lbs']} lbs</li>
                </ul>
                <ul style='color:#2a3e5c; font-size:1.07em; margin:0 0 0 18px; padding-left:0;'>
                    {''.join([f'<li>{f}</li>' for f in suite['features']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
        # Two dog card for price_two_dogs_same_kennel
        if suite.get('price_two_dogs_same_kennel', 0) > 0:
            st.markdown(f"""
            <div style='background-color:#eaf0fb; border-radius:18px; padding:24px; margin-bottom:18px; box-shadow: 0 2px 8px #00000010;'>
                <h2 style='margin-bottom:4px; color:#2a3e5c;'><span style='font-size:1.3em;'>🏠</span> {suite['suite_name']} (2 Dogs - Shared Kennel)</h2>
                <span style='font-size:2em; color:#fcbf49; font-weight:bold;'>${int(suite['price_two_dogs_same_kennel'])}</span><span style='color:#fcbf49;'>/night</span><br>
                <ul style='margin:10px 0 6px 0; padding-left:18px;'>
                    <li>{suite.get('suite_length', '')}x{suite.get('suite_width', '')} ft Indoor Suite</li>
                    <li>{suite['potty_breaks']} Daily Potty Break{'s' if suite['potty_breaks']!=1 else ''}</li>
                    <li>Accommodates up to {suite['accommodates_lbs']} lbs</li>
                </ul>
                <ul style='color:#2a3e5c; font-size:1.07em; margin:0 0 0 18px; padding-left:0;'>
                    {''.join([f'<li>{f}</li>' for f in suite['features']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)

st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: small;'>
Best Friends Pet Care - Kennel Suite Builder © 2025
</div>""", unsafe_allow_html=True)