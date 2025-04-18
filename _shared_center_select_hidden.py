import streamlit as st
import pandas as pd

def center_manager_selector():
    # Load and normalize center data
    center_df = pd.read_excel("Best Friends Location Info.xlsx")
    center_df.columns = [c.strip().lower() for c in center_df.columns]
    manager_col = "district manager"
    center_col = "ctr name"
    address_col = "full address"
    manager_list = sorted(center_df[manager_col].dropna().unique())

    # Use session state to persist selection across pages
    if "district_manager" not in st.session_state:
        st.session_state.district_manager = manager_list[0]
    if "ctr_name" not in st.session_state:
        filtered_centers = center_df[center_df[manager_col] == st.session_state.district_manager]
        st.session_state.ctr_name = filtered_centers[center_col].dropna().unique()[0]

    st.header("Center & Manager Information")
    dm_selected = st.selectbox("Select your District Manager", manager_list, index=manager_list.index(st.session_state.district_manager))
    filtered_centers = center_df[center_df[manager_col] == dm_selected]
    center_names = filtered_centers[center_col].dropna().unique()
    center_selected = st.selectbox("Select your Center", center_names, index=list(center_names).index(st.session_state.ctr_name) if st.session_state.ctr_name in center_names else 0)
    center_row = filtered_centers[filtered_centers[center_col] == center_selected].iloc[0]
    full_address = center_row.get(address_col, "")

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
