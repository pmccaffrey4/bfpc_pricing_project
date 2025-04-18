import streamlit as st
import pandas as pd
import uuid

st.set_page_config(page_title="Best Friends Pet Care Center Pricing", layout="wide")

# --- Load center data ---
center_df = pd.read_excel("Best Friends Location Info.xlsx")
# Normalize column names for robust access
center_df.columns = [c.strip().lower() for c in center_df.columns]

# Use correct column names from your sheet
manager_col = "district manager"
center_col = "ctr name"
address_col = "full address"

manager_list = sorted(center_df[manager_col].dropna().unique())

# --- District Manager selection ---
st.header("Center & Manager Information")
dm_selected = st.selectbox("Select your District Manager", manager_list)
filtered_centers = center_df[center_df[manager_col] == dm_selected]
center_names = filtered_centers[center_col].dropna().unique()
center_selected = st.selectbox("Select your Center", center_names)
center_row = filtered_centers[filtered_centers[center_col] == center_selected].iloc[0]
full_address = center_row.get(address_col, "")

st.markdown(f"**Selected Center:** {center_selected}")
st.markdown(f"**Full Address:** {full_address}")
st.markdown(f"**District Manager:** {dm_selected}")

st.image("bf_logo.png", width=120)
st.title("Best Friends Pet Care Center Pricing")

st.write("""
Use this form to add each type of kennel suite you offer. Fill out the details for each suite, then click 'Add Suite'. All added suites will be shown below as summary cards.
""")

# --- Kennel Suite Entry ---
if "kennel_suites" not in st.session_state:
    st.session_state.kennel_suites = []

with st.form("add_kennel_suite_form"):
    suite_name_options = ["Standard", "Large", "Luxury", "Cat", "Cat Luxury", "Other"]
    suite_name = st.selectbox("Suite Name", suite_name_options)
    suite_name_custom = ""
    if suite_name == "Other":
        suite_name_custom = st.text_input("Please specify suite name")
    final_suite_name = suite_name_custom.strip() if suite_name == "Other" else suite_name

    dog_size = st.selectbox(
        "Size of dog",
        ["small", "medium", "big", "extra big"]
    )
    price_per_night = st.number_input("Price per Dog per Night ($)", min_value=0.0, step=1.0)
    price_two_dogs_same_kennel = st.number_input("Price per Night for 2 Dogs ($) - Shared Kennel", min_value=0.0, step=1.0)
    num_kennels = st.number_input("Number of kennels of this type", min_value=0, step=1, format="%d")

    features = st.text_area(
        "Bulleted List of Features (one per line)",
        placeholder="e.g. climate controlled\nelevated beds"
    )
    submitted = st.form_submit_button("Add Suite")
    error_msg = ""
    # Prevent duplicate suites (same name + dog size)
    duplicate = any(s["suite_name"].lower() == final_suite_name.lower() and s["dog_size"] == dog_size for s in st.session_state.kennel_suites)
    if submitted:
        if suite_name == "Other" and not final_suite_name:
            error_msg = "Please enter a custom suite name."
        elif duplicate:
            error_msg = f"A suite with the name '{final_suite_name}' and dog size '{dog_size}' already exists."
        else:
            st.session_state.kennel_suites.append({
                "id": str(uuid.uuid4()),
                "suite_name": final_suite_name,
                "dog_size": dog_size,
                "price_per_night": price_per_night,
                "price_two_dogs_same_kennel": price_two_dogs_same_kennel,
                "num_kennels": num_kennels,
                "features": [f.strip() for f in features.split("\n") if f.strip()],
                "ctr_name": center_selected,
                "full_address": full_address,
                "district_manager": dm_selected,
            })
            st.success(f"Added suite: {final_suite_name}")
    if error_msg:
        st.error(error_msg)

# --- Display Suites as Cards ---
if st.session_state.kennel_suites:
    st.subheader("Current Suites")
    for suite in st.session_state.kennel_suites:
        # Single dog card
        st.markdown(f"""
        <div style='background-color:#eaf0fb; border-radius:18px; padding:24px; margin-bottom:18px; box-shadow: 0 2px 8px #00000010;'>
            <h2 style='margin-bottom:4px; color:#2a3e5c;'><span style='font-size:1.3em;'>🏠</span> {suite['suite_name']} (1 Dog)</h2>
            <span style='font-size:2em; color:#fcbf49; font-weight:bold;'>${int(suite['price_per_night'])}</span><span style='color:#fcbf49;'>/night</span><br>
            <ul style='margin:10px 0 6px 0; padding-left:18px; color:#000;'>
                <li><b>District Manager:</b> {suite['district_manager']}</li>
                <li><b>Center Name:</b> {suite['ctr_name']}</li>
                <li><b>Full Address:</b> {suite['full_address']}</li>
                <li>Dog size: {suite['dog_size']}</li>
                <li>Number of kennels: {suite['num_kennels']}</li>
            </ul>
            <div style='margin:10px 0 0 18px;'>
                <strong style='color:#000;'>Features:</strong>
                <ul style='color:#000; font-size:1.07em; margin:4px 0 0 0; padding-left:18px;'>
                    {''.join([f'<li>{f}</li>' for f in suite['features']])}
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        # Two dog card for price_two_dogs_same_kennel
        if suite.get('price_two_dogs_same_kennel', 0) > 0:
            st.markdown(f"""
            <div style='background-color:#eaf0fb; border-radius:18px; padding:24px; margin-bottom:18px; box-shadow: 0 2px 8px #00000010;'>
                <h2 style='margin-bottom:4px; color:#2a3e5c;'><span style='font-size:1.3em;'>🏠</span> {suite['suite_name']} (2 Dogs - Shared Kennel)</h2>
                <span style='font-size:2em; color:#fcbf49; font-weight:bold;'>${int(suite['price_two_dogs_same_kennel'])}</span><span style='color:#fcbf49;'>/night</span><br>
                <ul style='margin:10px 0 6px 0; padding-left:18px; color:#000;'>
                    <li><b>District Manager:</b> {suite['district_manager']}</li>
                    <li><b>Center Name:</b> {suite['ctr_name']}</li>
                    <li><b>Full Address:</b> {suite['full_address']}</li>
                    <li>Dog size: {suite['dog_size']}</li>
                    <li>Number of kennels: {suite['num_kennels']}</li>
                </ul>
                <div style='margin:10px 0 0 18px;'>
                    <strong style='color:#000;'>Features:</strong>
                    <ul style='color:#000; font-size:1.07em; margin:4px 0 0 0; padding-left:18px;'>
                        {''.join([f'<li>{f}</li>' for f in suite['features']])}
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: small;'>
Best Friends Pet Care - Kennel Suite Builder © 2025
</div>""", unsafe_allow_html=True)
