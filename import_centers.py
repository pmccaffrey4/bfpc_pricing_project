#!/usr/bin/env python3
"""
Script to import Best Friends Location Info from Excel to Supabase.
Run this once to populate the centers table with location data.
"""

import pandas as pd
import streamlit as st
from supabase_config import get_supabase_client, save_to_supabase
import sys

def import_centers_from_excel(excel_file="Best Friends Location Info.xlsx"):
    """Import center data from Excel to Supabase centers table."""
    print(f"Reading data from {excel_file}...")
    
    try:
        # Load Excel data
        center_df = pd.read_excel(excel_file)
        # Normalize column names
        center_df.columns = [c.strip().lower() for c in center_df.columns]
        
        # Map Excel columns to database columns (lowercase in Excel)
        col_map = {
            "ctr_cd": "ctr_cd",                      # Center code
            "ctr name": "ctr_name",                  # Center name
            "is_open": "is_open",                    # Is the center open
            "is_acquisition": "is_acquisition",      # Is this an acquisition
            "full address": "full_address",          # Full address
            "state": "state",                        # State
            "zipcode": "zipcode",                    # Zip code
            "nelson dma": "nelson_dma",              # Nielsen DMA 
            "dma code": "dma_code",                  # DMA code
            "district manager": "district_manager",  # District manager
            "market manager": "market_manager",      # Market manager
            "center manager": "center_manager",      # Center manager
            "crm email": "crm_email",               # CRM email
            "services": "services",                  # Services offered
            "system": "system",                      # System
            "website": "website",                    # Website URL
            "google ads account": "google_ads_account",        # Google Ads account
            "google ads reports links": "google_ads_reports_links"  # Google Ads reports links
        }
        
        # Required columns check
        required_cols = ["district manager", "ctr name"]
        missing_cols = [col for col in required_cols if col not in center_df.columns]
        if missing_cols:
            print(f"Error: Missing required columns in Excel: {missing_cols}")
            return False
        
        # Get Supabase client
        client = get_supabase_client()
        
        # Optional: Clear existing data
        if len(sys.argv) > 1 and sys.argv[1] == "--clear":
            print("Clearing existing centers table...")
            client.table("centers").delete().execute()
            print("Existing data cleared.")
        
        # Insert each row into Supabase
        success_count = 0
        error_count = 0
        
        print(f"Found {len(center_df)} centers to import.")
        for _, row in center_df.iterrows():
            # Prepare data with all available columns from Excel
            center_data = {}
            
            # Map all available columns from Excel to DB fields
            for excel_col, db_col in col_map.items():
                if excel_col in row.index:
                    # Handle special case for boolean fields
                    if db_col in ["is_open", "is_acquisition"]:
                        # Convert to boolean (1, yes, true, etc.)
                        value = row[excel_col]
                        if isinstance(value, (int, float)):
                            center_data[db_col] = bool(value)
                        elif isinstance(value, str):
                            center_data[db_col] = value.lower() in ["yes", "true", "1", "t", "y"]
                        else:
                            center_data[db_col] = False
                    else:
                        # Regular field, convert NaN to empty string
                        value = row[excel_col]
                        if pd.isna(value):
                            value = ""
                        center_data[db_col] = value
            
            # Skip rows with missing required data
            if not center_data.get("ctr_name") or not center_data.get("district_manager"):
                print(f"Skipping row with missing required data")
                error_count += 1
                continue
                
            # Add active flag
            center_data["active"] = True
            
            # Save to Supabase
            try:
                response = client.table("centers").insert(center_data).execute()
                if response.data:
                    success_count += 1
                else:
                    print(f"Error importing: {center_data}")
                    error_count += 1
            except Exception as e:
                print(f"Exception importing {center_data['center_name']}: {str(e)}")
                error_count += 1
        
        print(f"Import completed: {success_count} centers imported successfully, {error_count} errors.")
        return success_count > 0
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    # This allows the script to be run from command line: python import_centers.py [--clear]
    import_centers_from_excel()
