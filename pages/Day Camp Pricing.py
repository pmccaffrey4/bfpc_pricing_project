import streamlit as st
import uuid
from _shared_center_select_hidden import center_manager_selector

st.set_page_config(page_title="Day Camp Pricing", layout="wide")
dm_selected, center_selected, full_address = center_manager_selector()
st.image("bf_logo.png", width=120)
st.title("Best Friends Day Camp Pricing")

st.write("""
Use this form to add your Day Camp pricing options. Fill out the details for each daily option and package, then click 'Add'. All added options will be shown below as summary cards.
""")

# --- Daily Options ---
st.header("Daily Options")
if "daycamp_daily" not in st.session_state:
    st.session_state.daycamp_daily = None

with st.form("submit_daily_options"):
    col1, col2, col3 = st.columns(3)
    with col1:
        daily_dropin_price = st.number_input("Daily Drop-In Price ($)", min_value=0.0, step=1.0, value=28.0, key="dropin")
        st.text("Full Day of Play\nGroup Activities\nRegular Exercise\nDaily Updates")
    with col2:
        half_day_price = st.number_input("Half-Day Price ($)", min_value=0.0, step=1.0, value=14.0, key="halfday")
        st.text("Under 4 Hours\nPerfect with Grooming\nGroup Activities\nRegular Exercise")
    with col3:
        weekend_price = st.number_input("Weekend Price ($)", min_value=0.0, step=1.0, value=14.0, key="weekend")
        st.text("Full Day of Play\nGroup Activities\nRegular Exercise\nDaily Updates")
    daily_submitted = st.form_submit_button("Submit Daily Options")
    if daily_submitted:
        st.session_state.daycamp_daily = {
            "dropin": daily_dropin_price,
            "halfday": half_day_price,
            "weekend": weekend_price
        }

# --- Daycamp Packages ---
st.header("Daycamp Packages")
if "daycamp_packages" not in st.session_state:
    st.session_state.daycamp_packages = []

with st.form("add_daycamp_package_form"):
    package_days = st.number_input("Number of Days in Package", min_value=1, step=1)
    package_price = st.number_input("Package Price ($)", min_value=0.0, step=1.0)
    package_expiration = st.text_input("Expiration Policy (e.g., 30-day expiration)")
    submitted = st.form_submit_button("Add Package")
    if submitted:
        st.session_state.daycamp_packages.append({
            "id": str(uuid.uuid4()),
            "days": package_days,
            "price": package_price,
            "expiration": package_expiration
        })
        st.success(f"Added {package_days}-Day Package")

if st.session_state.daycamp_packages:
    st.subheader("Current Packages")
    for pkg in st.session_state.daycamp_packages:
        st.markdown(f"""
        <div style='background-color:#eaf0fb; border-radius:18px; padding:18px; margin-bottom:10px; box-shadow: 0 2px 8px #00000010;'>
            <h3 style='color:#2a3e5c;'>{pkg['days']}-Day Package</h3>
            <span style='font-size:1.6em; color:#fcbf49; font-weight:bold;'>${int(pkg['price'])}</span><br>
            <span style='color:gray;'>Expiration: {pkg['expiration']}</span>
        </div>
        """, unsafe_allow_html=True)

# --- Daily Options Summary ---
if st.session_state.get("daycamp_daily"):
    st.subheader("Current Daily Options")
    daily = st.session_state.daycamp_daily
    st.markdown(f"""
    <div style='background-color:#eaf0fb; border-radius:18px; padding:18px; margin-bottom:10px; box-shadow: 0 2px 8px #00000010;'>
        <h3 style='color:#2a3e5c;'>Daily Drop-In</h3>
        <span style='font-size:1.6em; color:#fcbf49; font-weight:bold;'>${daily['dropin']:.2f}</span> <span style='color:gray;'>/day</span><br>
        <ul><li>Full Day of Play</li><li>Group Activities</li><li>Regular Exercise</li><li>Daily Updates</li></ul>
        <h3 style='color:#2a3e5c;'>Half-Day</h3>
        <span style='font-size:1.6em; color:#fcbf49; font-weight:bold;'>${daily['halfday']:.2f}</span> <span style='color:gray;'>/day</span><br>
        <ul><li>Under 4 Hours</li><li>Perfect with Grooming</li><li>Group Activities</li><li>Regular Exercise</li></ul>
        <h3 style='color:#2a3e5c;'>Weekends</h3>
        <span style='font-size:1.6em; color:#fcbf49; font-weight:bold;'>${daily['weekend']:.2f}</span> <span style='color:gray;'>/day</span><br>
        <ul><li>Full Day of Play</li><li>Group Activities</li><li>Regular Exercise</li><li>Daily Updates</li></ul>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: small;'>
Best Friends Pet Care - Day Camp Pricing © 2025
</div>""", unsafe_allow_html=True)
