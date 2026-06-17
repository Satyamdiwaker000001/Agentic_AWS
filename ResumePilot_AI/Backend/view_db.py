import sqlite3

def view_database(db_path="resumepilot.db"):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get list of all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            print("The database exists but has no tables yet.")
            return

        print(f"Found {len(tables)} tables in the database:\n")
        
        # Print content of each table
        for (table_name,) in tables:
            print(f"=== Table: {table_name} ===")
            
            # Get column names
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]
            print(" | ".join(columns))
            print("-" * 50)
            
            # Get rows
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            if not rows:
                print("(Table is empty)\n")
            else:
                for row in rows:
                    print(" | ".join(str(item) for item in row))
                print("\n")
                
        conn.close()
        
    except Exception as e:
        print(f"Error reading database: {e}")

if __name__ == "__main__":
    view_database()
