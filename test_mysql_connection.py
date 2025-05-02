import mysql.connector
import sys

def test_mysql_connection():
    # Database connection parameters from your Django settings
    db_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',  # Changed from 'mihai' to 'root'
        'password': 'Molly@2025',
        'database': 'lmd',
    }
    
    try:
        print("Attempting to connect to MySQL database...")
        connection = mysql.connector.connect(**db_config)
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Successfully connected to MySQL Server version {db_info}")
            
            cursor = connection.cursor()
            cursor.execute("SELECT database();")
            record = cursor.fetchone()
            print(f"Connected to database: {record[0]}")
            
            # Test executing a simple query
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            if tables:
                print("Tables in the database:")
                for table in tables:
                    print(f"- {table[0]}")
            else:
                print("No tables found in the database.")
                
            cursor.close()
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("MySQL connection is closed.")
    
    return True

if __name__ == "__main__":
    success = test_mysql_connection()
    sys.exit(0 if success else 1)