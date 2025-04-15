import streamlit as st
from supabase import create_client, Client

def get_supabase_client():
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    return create_client(url, key)
