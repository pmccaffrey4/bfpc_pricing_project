import streamlit as st
import json
from datetime import datetime
from supabase import create_client, Client
from typing import Dict, Any, Tuple, List, Optional, Union

def get_supabase_client() -> Client:
    """Create and return a Supabase client using credentials from Streamlit secrets."""
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    return create_client(url, key)


def save_to_supabase(table_name: str, data: Dict[str, Any]) -> Tuple[bool, str]:
    """Save data to Supabase table and return success status and message.
    
    Args:
        table_name: Name of the table to insert data into
        data: Dictionary of data to insert
        
    Returns:
        Tuple of (success, message)
    """
    try:
        client = get_supabase_client()
        response = client.table(table_name).insert(data).execute()
        
        # Check if response contains data (success)
        if response.data:
            return True, "Data saved successfully!"
        else:
            return False, f"Error: {response.error.message if hasattr(response, 'error') else 'Unknown error'}"
    except Exception as e:
        return False, f"Error: {str(e)}"


def fetch_from_supabase(table_name: str, center_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """Fetch data from Supabase with optional filtering by center name.
    
    Args:
        table_name: Name of the table to fetch data from
        center_name: Optional filter by center name
        
    Returns:
        List of records as dictionaries
    """
    try:
        client = get_supabase_client()
        query = client.table(table_name).select("*")
        
        if center_name:
            query = query.eq("center_name", center_name)
            
        response = query.execute()
        return response.data
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return []


def delete_from_supabase(table_name: str, id_value: str) -> Tuple[bool, str]:
    """Delete a record from Supabase table by ID.
    
    Args:
        table_name: Name of the table to delete from
        id_value: UUID of the record to delete
        
    Returns:
        Tuple of (success, message)
    """
    try:
        client = get_supabase_client()
        response = client.table(table_name).delete().eq("id", id_value).execute()
        
        if response.data:
            return True, "Record deleted successfully!"
        else:
            return False, f"Error: {response.error.message if hasattr(response, 'error') else 'No record found or error deleting'}"
    except Exception as e:
        return False, f"Error: {str(e)}"
