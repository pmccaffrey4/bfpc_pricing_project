import streamlit as st
import uuid
import json
import pandas as pd
from datetime import datetime
from _shared_center_select_hidden import center_manager_selector
from supabase_config import save_to_supabase, fetch_from_supabase, delete_from_supabase

st.set_page_config(page_title="Review & Submit", layout="wide")

# Use the shared center selector
dm_selected, center_selected, full_address = center_manager_selector()

st.image("bf_logo.png", width=120)
st.title("Review & Submit")

st.markdown("""
This page shows all of your pricing data for review. You can:
- Review all entries for accuracy
- Edit any entry to fix errors
- Delete entries that were created by mistake
- Submit final pricing data when everything looks correct
""")

# Function to pretty-format JSON
def format_json(json_data):
    return json.dumps(json_data, indent=2)

# Function to refresh data for a specific center
def fetch_all_center_data(center_name):
    """Fetch all data for a specific center from all tables"""
    kennel_suites = fetch_from_supabase("kennel_suites", center_name)
    daycamp_daily = fetch_from_supabase("daycamp_daily", center_name)
    daycamp_packages = fetch_from_supabase("daycamp_packages", center_name)
    
    return {
        "kennel_suites": kennel_suites,
        "daycamp_daily": daycamp_daily,
        "daycamp_packages": daycamp_packages
    }

# Function to handle data deletion
def handle_delete(table_name, record_id):
    success, message = delete_from_supabase(table_name, record_id)
    if success:
        st.success(f"✅ Record deleted successfully.")
        return True
    else:
        st.error(f"Error deleting record: {message}")
        return False

# Function to update record in Supabase
def update_record(table_name, record_id, updated_data):
    """Updates a record in Supabase"""
    try:
        client = get_supabase_client()
        response = client.table(table_name).update(updated_data).eq("id", record_id).execute()
        if response.data:
            return True, "Record updated successfully!"
        else:
            return False, f"Error: {response.error.message if hasattr(response, 'error') else 'Unknown error'}"
    except Exception as e:
        return False, f"Error: {str(e)}"

# Fetch all data for this center
if "center_data" not in st.session_state or st.button("Refresh Data"):
    st.session_state.center_data = fetch_all_center_data(center_selected)
    st.success("Data refreshed!")

# Create tabs for different data types
boarding_tab, daycamp_tab = st.tabs(["Boarding Pricing", "Day Camp Pricing"])

# --- Boarding Pricing Tab ---
with boarding_tab:
    st.header("Boarding Kennel Suites")
    kennel_data = st.session_state.center_data["kennel_suites"]
    
    if not kennel_data:
        st.info("No kennel suite data found for this center. Please add kennel suites in the Boarding Pricing page.")
    else:
        st.write(f"Found {len(kennel_data)} kennel suite entries.")
        
        # Display each kennel suite with edit/delete options
        for i, suite in enumerate(kennel_data):
            with st.expander(f"**{suite['suite_name']}** - {suite['dog_size']} - ${suite['price_per_night']}/night", expanded=i==0):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Display card with suite details
                    st.markdown(f"""
                    <div style='background-color:#eaf0fb; border-radius:18px; padding:24px; margin-bottom:18px; box-shadow: 0 2px 8px #00000010;'>
                        <h2 style='margin-bottom:4px; color:#2a3e5c;'><span style='font-size:1.3em;'>🏠</span> {suite['suite_name']} ({suite['dog_size']})</h2>
                        <span style='font-size:2em; color:#fcbf49; font-weight:bold;'>${int(suite['price_per_night'])}</span><span style='color:#fcbf49;'>/night</span><br>
                        <ul style='margin:10px 0 6px 0; padding-left:18px; color:#000;'>
                            <li>Number of kennels: {suite['num_kennels']}</li>
                            {f'<li>Two dogs price: ${int(suite["price_two_dogs_same_kennel"])}/night</li>' if suite.get('price_two_dogs_same_kennel') else ''}
                        </ul>
                        <div style='margin:10px 0 0 18px;'>
                            <strong style='color:#000;'>Features:</strong>
                            <ul style='color:#000; font-size:1.07em; margin:4px 0 0 0; padding-left:18px;'>
                                {''.join([f'<li>{f}</li>' for f in suite.get('features', [])])}
                            </ul>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Edit form for this suite
                    with st.form(key=f"edit_kennel_{suite['id']}"):
                        st.subheader("Edit Suite")
                        
                        # Edit fields
                        edit_suite_name = st.text_input("Suite Name", value=suite['suite_name'])
                        edit_dog_size = st.selectbox("Dog Size", 
                                                  ["small", "medium", "big", "extra big"],
                                                  index=["small", "medium", "big", "extra big"].index(suite['dog_size']) if suite['dog_size'] in ["small", "medium", "big", "extra big"] else 0)
                        edit_price = st.number_input("Price per Night ($)", 
                                                 min_value=0.0, 
                                                 value=float(suite['price_per_night']))
                        edit_two_dogs_price = st.number_input("Price for Two Dogs ($)", 
                                                         min_value=0.0, 
                                                         value=float(suite.get('price_two_dogs_same_kennel', 0)))
                        edit_num_kennels = st.number_input("Number of Kennels", 
                                                      min_value=0, 
                                                      value=int(suite['num_kennels']))
                        
                        # Features as multi-line text area
                        features_text = "\n".join(suite.get('features', []))
                        edit_features = st.text_area("Features (one per line)", 
                                                 value=features_text)
                        
                        # Parse features from text area
                        edit_features_list = [f.strip() for f in edit_features.split("\n") if f.strip()]
                        
                        # Update and Delete buttons
                        col_a, col_b = st.columns(2)
                        with col_a:
                            update_submitted = st.form_submit_button("Update")
                        with col_b:
                            delete_submitted = st.form_submit_button("Delete", type="secondary")
                        
                        # Handle update
                        if update_submitted:
                            updated_data = {
                                "suite_name": edit_suite_name,
                                "dog_size": edit_dog_size,
                                "price_per_night": edit_price,
                                "price_two_dogs_same_kennel": edit_two_dogs_price if edit_two_dogs_price > 0 else None,
                                "num_kennels": edit_num_kennels,
                                "features": edit_features_list,
                                "updated_at": datetime.utcnow().isoformat()
                            }
                            
                            success, message = update_record("kennel_suites", suite["id"], updated_data)
                            if success:
                                st.success("✅ Suite updated successfully!")
                                # Refresh data to show changes
                                st.session_state.center_data = fetch_all_center_data(center_selected)
                                st.rerun()
                            else:
                                st.error(f"Error updating suite: {message}")
                        
                        # Handle delete
                        if delete_submitted:
                            if handle_delete("kennel_suites", suite["id"]):
                                # Refresh data to reflect deletion
                                st.session_state.center_data = fetch_all_center_data(center_selected)
                                st.rerun()

# --- Day Camp Pricing Tab ---
with daycamp_tab:
    col1, col2 = st.columns(2)
    
    # Daily Options Section
    with col1:
        st.subheader("Daily Options")
        daily_data = st.session_state.center_data["daycamp_daily"]
        
        if not daily_data:
            st.info("No daily options found. Please add them in the Day Camp Pricing page.")
        else:
            # Use the most recent submission (should be only one per center)
            daily = daily_data[0]
            
            # Display current values
            st.markdown(f"""
            <div style='background-color:#eaf0fb; border-radius:18px; padding:18px; margin-bottom:10px; box-shadow: 0 2px 8px #00000010;'>
                <h3 style='color:#2a3e5c;'>Daily Drop-In</h3>
                <span style='font-size:1.6em; color:#fcbf49; font-weight:bold;'>${daily['dropin']:.2f}</span> <span style='color:gray;'>/day</span><br>
                <h3 style='color:#2a3e5c;'>Half-Day</h3>
                <span style='font-size:1.6em; color:#fcbf49; font-weight:bold;'>${daily['halfday']:.2f}</span> <span style='color:gray;'>/day</span><br>
                <h3 style='color:#2a3e5c;'>Weekends</h3>
                <span style='font-size:1.6em; color:#fcbf49; font-weight:bold;'>${daily['weekend']:.2f}</span> <span style='color:gray;'>/day</span><br>
            </div>
            """, unsafe_allow_html=True)
            
            # Edit form for daily options
            with st.form(key=f"edit_daily_{daily['id']}"):
                st.subheader("Edit Daily Options")
                
                # Edit fields
                edit_dropin = st.number_input("Daily Drop-In Price ($)", 
                                         min_value=0.0, 
                                         value=float(daily['dropin']))
                edit_halfday = st.number_input("Half-Day Price ($)", 
                                          min_value=0.0, 
                                          value=float(daily['halfday']))
                edit_weekend = st.number_input("Weekend Price ($)", 
                                          min_value=0.0, 
                                          value=float(daily['weekend']))
                
                # Update and Delete buttons
                col_a, col_b = st.columns(2)
                with col_a:
                    update_daily = st.form_submit_button("Update")
                with col_b:
                    delete_daily = st.form_submit_button("Delete", type="secondary")
                
                # Handle update
                if update_daily:
                    updated_data = {
                        "dropin": edit_dropin,
                        "halfday": edit_halfday,
                        "weekend": edit_weekend,
                        "updated_at": datetime.utcnow().isoformat()
                    }
                    
                    success, message = update_record("daycamp_daily", daily["id"], updated_data)
                    if success:
                        st.success("✅ Daily options updated successfully!")
                        # Refresh data to show changes
                        st.session_state.center_data = fetch_all_center_data(center_selected)
                        st.rerun()
                    else:
                        st.error(f"Error updating daily options: {message}")
                
                # Handle delete
                if delete_daily:
                    if handle_delete("daycamp_daily", daily["id"]):
                        # Refresh data to reflect deletion
                        st.session_state.center_data = fetch_all_center_data(center_selected)
                        st.rerun()
    
    # Packages Section
    with col2:
        st.subheader("Day Camp Packages")
        packages_data = st.session_state.center_data["daycamp_packages"]
        
        if not packages_data:
            st.info("No packages found. Please add them in the Day Camp Pricing page.")
        else:
            st.write(f"Found {len(packages_data)} day camp packages.")
            
            # Display each package with edit/delete options
            for package in packages_data:
                with st.expander(f"{package['days']}-Day Package - ${package['price']}"):
                    # Display package details
                    st.markdown(f"""
                    <div style='background-color:#eaf0fb; border-radius:18px; padding:18px; margin-bottom:10px; box-shadow: 0 2px 8px #00000010;'>
                        <h3 style='color:#2a3e5c;'>{package['days']}-Day Package</h3>
                        <span style='font-size:1.6em; color:#fcbf49; font-weight:bold;'>${int(package['price'])}</span><br>
                        <span style='color:gray;'>Expiration: {package.get('expiration', 'N/A')}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Edit form for this package
                    with st.form(key=f"edit_package_{package['id']}"):
                        # Edit fields
                        edit_days = st.number_input("Number of Days", 
                                              min_value=1, 
                                              value=int(package['days']))
                        edit_price = st.number_input("Package Price ($)", 
                                               min_value=0.0, 
                                               value=float(package['price']))
                        edit_expiration = st.text_input("Expiration Policy", 
                                                  value=package.get('expiration', ''))
                        
                        # Update and Delete buttons
                        col_a, col_b = st.columns(2)
                        with col_a:
                            update_package = st.form_submit_button("Update")
                        with col_b:
                            delete_package = st.form_submit_button("Delete", type="secondary")
                        
                        # Handle update
                        if update_package:
                            updated_data = {
                                "days": edit_days,
                                "price": edit_price,
                                "expiration": edit_expiration,
                                "updated_at": datetime.utcnow().isoformat()
                            }
                            
                            success, message = update_record("daycamp_packages", package["id"], updated_data)
                            if success:
                                st.success("✅ Package updated successfully!")
                                # Refresh data to show changes
                                st.session_state.center_data = fetch_all_center_data(center_selected)
                                st.rerun()
                            else:
                                st.error(f"Error updating package: {message}")
                        
                        # Handle delete
                        if delete_package:
                            if handle_delete("daycamp_packages", package["id"]):
                                # Refresh data to reflect deletion
                                st.session_state.center_data = fetch_all_center_data(center_selected)
                                st.rerun()

# Add a "Final Submit" button that confirms all data is correct
st.divider()
st.header("Final Submission")
st.markdown("""
Once you've reviewed all your pricing data and made any necessary corrections, 
click the button below to finalize your submission.
""")

# Check if we have at least one piece of data for this center
has_data = (
    len(st.session_state.center_data["kennel_suites"]) > 0 or 
    len(st.session_state.center_data["daycamp_daily"]) > 0 or 
    len(st.session_state.center_data["daycamp_packages"]) > 0
)

if not has_data:
    st.warning("You don't have any pricing data yet. Please add data in the Boarding Pricing and Day Camp Pricing pages before submitting.")
else:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Submit Final Pricing Data", type="primary", use_container_width=True):
            # Here we could add additional finalization logic if needed
            # For example, marking records as "submitted" or sending notifications
            
            st.balloons()
            st.success("Thank you! Your pricing data has been successfully submitted.")
            
            # Display a summary
            with st.expander("Submission Summary", expanded=True):
                st.markdown("### Your Submitted Pricing Data")
                st.markdown(f"**Center:** {center_selected}")
                st.markdown(f"**District Manager:** {dm_selected}")
                st.markdown(f"**Submission Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                st.markdown("#### Kennel Suites")
                if len(st.session_state.center_data["kennel_suites"]) > 0:
                    for i, suite in enumerate(st.session_state.center_data["kennel_suites"]):
                        st.markdown(f"{i+1}. **{suite['suite_name']}** - {suite['dog_size']} - ${suite['price_per_night']}/night")
                else:
                    st.markdown("_No kennel suites submitted_")
                
                st.markdown("#### Day Camp Pricing")
                if len(st.session_state.center_data["daycamp_daily"]) > 0:
                    daily = st.session_state.center_data["daycamp_daily"][0]
                    st.markdown(f"Daily Drop-In: **${daily['dropin']}**")
                    st.markdown(f"Half-Day: **${daily['halfday']}**")
                    st.markdown(f"Weekend: **${daily['weekend']}**")
                else:
                    st.markdown("_No daily options submitted_")
                
                st.markdown("#### Day Camp Packages")
                if len(st.session_state.center_data["daycamp_packages"]) > 0:
                    for i, pkg in enumerate(st.session_state.center_data["daycamp_packages"]):
                        st.markdown(f"{i+1}. **{pkg['days']}-Day Package** - ${pkg['price']} - Expires: {pkg.get('expiration', 'N/A')}")
                else:
                    st.markdown("_No packages submitted_")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: small;'>
Best Friends Pet Care - Pricing Portal © 2025
</div>""", unsafe_allow_html=True)
