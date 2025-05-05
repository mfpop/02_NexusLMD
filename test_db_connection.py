import os
import sys
import django
from django.conf import settings

# Print Python version for debugging
print(f"Python version: {sys.version}")

# First, try to print current Django settings before initialization
try:
    print("Current settings module:", os.environ.get('DJANGO_SETTINGS_MODULE', 'Not set'))
except Exception as e:
    print(f"Error checking environment: {e}")

# Set up Django environment
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
try:
    django.setup()
    print("Django successfully initialized")
except Exception as e:
    print(f"Error during django.setup(): {e}")
    sys.exit(1)

# Check database configuration
print("\nDatabase Configuration:")
try:
    db_config = settings.DATABASES.get('default', {})
    engine = db_config.get('ENGINE', 'Not configured')
    name = db_config.get('NAME', 'Not configured')
    host = db_config.get('HOST', 'Not configured')
    print(f"ENGINE: {engine}")
    print(f"NAME: {name}")
    print(f"HOST: {host}")
except Exception as e:
    print(f"Error accessing settings: {e}")

# Try to establish a connection to check for issues
print("\nTesting database connection...")
try:
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()[0]
    print(f"Successfully connected to database. Version: {version}")
    
    # Check database type
    cursor.execute("SELECT @@version")
    full_version = cursor.fetchone()[0]
    print(f"Full database version: {full_version}")
    
    # Better MySQL detection - the version string by itself is sufficient for MySQL detection
    if cursor.execute("SHOW VARIABLES LIKE 'version_comment'"):
        version_comment = cursor.fetchone()[1]
        print(f"Database version comment: {version_comment}")
        if "MySQL" in version_comment:
            print("✅ Confirmed using MySQL database backend")
        else:
            # Even if the comment doesn't contain "MySQL", if we got here, we're connected to a MySQL-compatible database
            print("✅ Connected to a MySQL-compatible database")
    else:
        # If we're connected and the query works, it's MySQL
        print("✅ Using MySQL database backend (detected by successful connection)")
    
    # Check if MySQL database 'lmd' exists
    try:
        cursor.execute("SELECT DATABASE()")
        current_db = cursor.fetchone()[0]
        print(f"Currently connected to database: {current_db}")
    except Exception as db_e:
        print(f"Error checking current database: {db_e}")
    
    cursor.close()
except Exception as e:
    print(f"Connection error: {e}")
    
    # Check if it might be a MySQL configuration issue
    error_str = str(e).lower()
    if "unknown database" in error_str:
        print("\nThe 'lmd' database doesn't exist. Try creating it with:")
        print("1. Open MySQL command prompt: mysql -u root -p")
        print("2. Enter your password: Molly@2025")
        print("3. Create the database: CREATE DATABASE lmd;")
        print("4. Verify: SHOW DATABASES;")
    elif "access denied" in error_str:
        print("\nAuthentication failed. Check your MySQL credentials.")
    elif "can't connect" in error_str or "connection refused" in error_str:
        print("\nCould not connect to MySQL server. Make sure:")
        print("1. MySQL service is running (net start MySQL80)")
        print("2. The server is accessible at localhost:3306")
    
print("\nTest completed. Check the messages above for connection issues.")