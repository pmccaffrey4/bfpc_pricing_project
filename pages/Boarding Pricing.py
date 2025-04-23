import streamlit as st
import uuid
from datetime import datetime
from supabase_config import save_to_supabase, fetch_from_supabase, delete_from_supabase
from _shared_center_select_hidden import center_manager_selector

st.set_page_config(page_title="Best Friends Pet Care Center Pricing", layout="wide")

# Use the shared center selector (reads from Supabase with Excel fallback)
dm_selected, center_selected, full_address = center_manager_selector()
# The center info is already displayed in the center_manager_selector function

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

    dog_sizes = st.multiselect(
        "Dog sizes this kennel can accommodate",
        ["small", "medium", "big", "extra big"],
        default=["small"],
        help="Select all dog sizes this kennel type can accommodate"
    )
    price_per_night = st.number_input("Price per Dog per Night ($)", min_value=0.0, step=1.0)
    price_additional_dog = st.number_input("Price for Additional Dog in Same Kennel ($)", 
                                   min_value=0.0, step=1.0, 
                                   help="How much to charge for a second dog in the same kennel")
    num_kennels = st.number_input("Number of kennels of this type", min_value=0, step=1, format="%d")

    features = st.text_area(
        "Bulleted List of Features (one per line)",
        placeholder="e.g. climate controlled\nelevated beds"
    )
    submitted = st.form_submit_button("Add Suite")
    error_msg = ""
    # Prevent duplicate suites (just by name - one entry can now handle multiple dog sizes)
    duplicate = any(s["suite_name"].lower() == final_suite_name.lower() for s in st.session_state.kennel_suites)
    if submitted:
        if suite_name == "Other" and not final_suite_name:
            error_msg = "Please enter a custom suite name."
        elif duplicate:
            error_msg = f"A suite with the name '{final_suite_name}' already exists. Please use a different name."
        else:
            # Generate a unique ID
            suite_id = str(uuid.uuid4())
            
            # Prepare features as a list
            feature_list = [f.strip() for f in features.split("\n") if f.strip()]
            
            # Create suite data for session state
            suite_data = {
                "id": suite_id,
                "suite_name": final_suite_name,
                "dog_sizes": dog_sizes,
                "price_per_night": price_per_night,
                "price_additional_dog": price_additional_dog,
                "num_kennels": num_kennels,
                "features": feature_list,
                "ctr_name": center_selected,
                "full_address": full_address,
                "district_manager": dm_selected,
            }
            
            # Save to session state for UI display
            st.session_state.kennel_suites.append(suite_data)
            
            # Prepare data for Supabase
            supabase_data = {
                "id": suite_id,
                "center_name": center_selected,  # Match the database column name
                "district_manager": dm_selected,
                "full_address": full_address,
                "suite_name": final_suite_name,
                "dog_sizes": dog_sizes,  # Using the new JSONB column
                "price_per_night": price_per_night,
                "price_additional_dog": price_additional_dog,  # Using the renamed column
                "num_kennels": num_kennels,
                "features": feature_list  # Supabase will convert this to JSONB
            }
            
            # Save to Supabase
            success, message = save_to_supabase("kennel_suites", supabase_data)
            if success:
                st.success(f"Added suite: {final_suite_name} - ✅ Saved to database!")
            else:
                st.error(f"Suite added locally but failed to save to database: {message}")
    if error_msg:
        st.error(error_msg)

# --- Display Suites as Cards ---
if st.session_state.kennel_suites:
    st.subheader("Current Suites")
    for suite in st.session_state.kennel_suites:
        # Single dog card - updated to show all dog sizes
        st.markdown(f"""
        <div style='background-color:#eaf0fb; border-radius:18px; padding:24px; margin-bottom:18px; box-shadow: 0 2px 8px #00000010;'>
            <h2 style='margin-bottom:4px; color:#2a3e5c;'><span style='font-size:1.3em;'>🏠</span> {suite['suite_name']}</h2>
            <span style='font-size:2em; color:#fcbf49; font-weight:bold;'>${int(suite['price_per_night'])}</span><span style='color:#fcbf49;'>/night</span>
            {f'<span style="margin-left:15px; color:#6c757d;"><i>(+${int(suite.get("price_additional_dog", 0))} for additional dog)</i></span>' if suite.get('price_additional_dog', 0) > 0 else ''}<br>
            <ul style='margin:10px 0 6px 0; padding-left:18px; color:#000;'>
                <li><b>District Manager:</b> {suite['district_manager']}</li>
                <li><b>Center Name:</b> {suite['ctr_name']}</li>
                <li><b>Full Address:</b> {suite['full_address']}</li>
                <li><b>Compatible Dog Sizes:</b> {', '.join(suite['dog_sizes'])}</li>
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
        # We no longer need a separate card for 2 dogs

# Add a section for managing existing Supabase records
st.divider()
st.subheader("Data Management")

with st.expander("View Records in Supabase"):
    if st.button("Refresh Data", key="refresh_kennel_data"):
        st.subheader("Kennel Suites in Database")
        suite_records = fetch_from_supabase("kennel_suites", center_selected)
        if suite_records:
            for record in suite_records:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.json(record)
                with col2:
                    if st.button("Delete", key=f"delete_{record['id']}"):
                        success, message = delete_from_supabase("kennel_suites", record['id'])
                        if success:
                            st.success(f"✅ {message} Refresh to see changes.")
                        else:
                            st.error(message)
        else:
            st.info("No kennel suites found in database for this center.")

st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: small;'>
Best Friends Pet Care - Kennel Suite Builder © 2025
</div>""", unsafe_allow_html=True)
