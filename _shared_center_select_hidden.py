import streamlit as st
import pandas as pd
import os.path
from supabase_config import fetch_from_supabase

def center_manager_selector():
    # Check if we should use Supabase or fallback to Excel
    use_supabase = True
    
    # Fetch center data from Supabase
    try:
        centers_data = fetch_from_supabase("centers")
        
        if not centers_data:  # If no data in Supabase, fallback to Excel
            use_supabase = False
            st.warning("No centers found in database. Falling back to Excel file.")
    except Exception as e:
        use_supabase = False
        st.warning(f"Error connecting to database: {str(e)}. Falling back to Excel file.")
    
    # Decide data source based on availability
    if use_supabase:
        # Convert Supabase data to dataframe
        center_df = pd.DataFrame(centers_data)
        # Define column names from database
        manager_col = "district_manager"
        center_col = "ctr_name"  # Updated to match new column name
        address_col = "full_address"
    else:
        # Fallback to Excel file
        excel_file = "Best Friends Location Info.xlsx"
        if not os.path.exists(excel_file):
            st.error(f"Excel file {excel_file} not found. Please import centers data.")
            manager_list = ["No data available"]
            return "No data available", "No data available", "No data available"
            
        # Load and normalize center data from Excel
        center_df = pd.read_excel(excel_file)
        center_df.columns = [c.strip().lower() for c in center_df.columns]
        # Define column names from Excel
        manager_col = "district manager"
        center_col = "ctr name"
        address_col = "full address"
    
    # Get list of district managers
    manager_list = sorted(center_df[manager_col].dropna().unique())

    # Use session state to persist selection across pages
    if "district_manager" not in st.session_state or st.session_state.district_manager not in manager_list:
        st.session_state.district_manager = manager_list[0] if manager_list else "No data available"
        
    if "ctr_name" not in st.session_state:
        filtered_centers = center_df[center_df[manager_col] == st.session_state.district_manager]
        center_names = filtered_centers[center_col].dropna().unique() if not filtered_centers.empty else ["No centers available"]
        st.session_state.ctr_name = center_names[0] if len(center_names) > 0 else "No centers available"

    st.header("Center & Manager Information")
    
    # Display a short message indicating data source
    if use_supabase:
        st.caption("Using center data from database")
    else:
        st.caption("Using center data from Excel file")
    
    # District Manager selector
    dm_index = manager_list.index(st.session_state.district_manager) if st.session_state.district_manager in manager_list else 0
    dm_selected = st.selectbox("Select your District Manager", manager_list, index=dm_index)
    
    # Filter centers for selected manager
    filtered_centers = center_df[center_df[manager_col] == dm_selected]
    center_names = filtered_centers[center_col].dropna().unique() if not filtered_centers.empty else ["No centers available"]
    
    # Center selector with index safety
    center_index = list(center_names).index(st.session_state.ctr_name) if st.session_state.ctr_name in center_names else 0
    center_selected = st.selectbox("Select your Center", center_names, index=center_index)
    
    # Get full address and other details
    if not filtered_centers.empty and center_selected in filtered_centers[center_col].values:
        center_row = filtered_centers[filtered_centers[center_col] == center_selected].iloc[0]
        full_address = center_row.get(address_col, "")
    else:
        full_address = ""

    # Update session state if changed
    if dm_selected != st.session_state.district_manager:
        st.session_state.district_manager = dm_selected
        # Reset center to first available for new manager
        st.session_state.ctr_name = center_names[0]
    if center_selected != st.session_state.ctr_name:
        st.session_state.ctr_name = center_selected

    st.markdown(f"**Selected Center:** {center_selected}")
    st.markdown(f"**Full Address:** {full_address}")
    st.markdown(f"**District Manager:** {dm_selected}")

    return dm_selected, center_selected, full_address
