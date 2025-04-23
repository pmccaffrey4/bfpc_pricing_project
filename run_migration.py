import streamlit as st
import os
from supabase_config import get_supabase_client
import sys

def run_migration(migration_file):
    """Run a SQL migration file against the Supabase database"""
    print(f"Running migration from file: {migration_file}")
    
    # Check if file exists
    if not os.path.exists(migration_file):
        print(f"Error: Migration file {migration_file} not found.")
        return False
    
    try:
        # Read the migration SQL
        with open(migration_file, 'r') as f:
            migration_sql = f.read()
        
        # Split the migration into individual statements
        # This simple split won't work for all SQL, but should be ok for our basic migration
        sql_statements = [stmt.strip() for stmt in migration_sql.split(';') if stmt.strip()]
        
        # Get Supabase client
        client = get_supabase_client()
        
        # Execute each statement
        for i, stmt in enumerate(sql_statements, 1):
            if not stmt:
                continue
                
            print(f"Executing statement {i}/{len(sql_statements)}...")
            
            # Use the rpc function to execute raw SQL
            response = client.rpc('execute_sql', {'query': stmt}).execute()
            
            if hasattr(response, 'error') and response.error:
                print(f"Error executing statement {i}: {response.error}")
                return False
                
            print(f"Statement {i} executed successfully.")
        
        print("Migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error during migration: {str(e)}")
        return False

if __name__ == "__main__":
    # Get migration file from command line argument or use default
    migration_file = sys.argv[1] if len(sys.argv) > 1 else "sql/migrations/update_kennel_suites_table.sql"
    
    # Run the migration
    success = run_migration(migration_file)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
