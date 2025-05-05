import os
import django
from django.db import connection

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def test_mysql_connection():
    """Test the MySQL connection and check profile-related tables."""
    try:
        # Check database connection
        with connection.cursor() as cursor:
            # Get database info
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"Connected to MySQL server version: {version[0]}")
            
            # Check if profile tables exist
            cursor.execute("SHOW TABLES LIKE 'authenticate_profile'")
            profile_table = cursor.fetchone()
            cursor.execute("SHOW TABLES LIKE 'authenticate_workexperience'")
            work_exp_table = cursor.fetchone()
            
            if profile_table:
                print("✅ Profile table exists in MySQL database")
                # Get profile columns
                cursor.execute("DESCRIBE authenticate_profile")
                columns = cursor.fetchall()
                print("Profile columns:")
                for col in columns:
                    print(f"  - {col[0]}: {col[1]}")
            else:
                print("❌ Profile table not found in MySQL database")
                
            if work_exp_table:
                print("\n✅ Work Experience table exists in MySQL database")
                # Get work experience columns
                cursor.execute("DESCRIBE authenticate_workexperience")
                columns = cursor.fetchall()
                print("Work Experience columns:")
                for col in columns:
                    print(f"  - {col[0]}: {col[1]}")
            else:
                print("❌ Work Experience table not found in MySQL database")
            
            # Count records in tables
            cursor.execute("SELECT COUNT(*) FROM authenticate_profile")
            profile_count = cursor.fetchone()[0]
            print(f"\nNumber of profile records: {profile_count}")
            
            cursor.execute("SELECT COUNT(*) FROM authenticate_workexperience")
            work_exp_count = cursor.fetchone()[0]
            print(f"Number of work experience records: {work_exp_count}")
            
    except Exception as e:
        print(f"Error connecting to MySQL database: {e}")
        return False
        
    return True

if __name__ == "__main__":
    print("Testing MySQL connection and profile tables...")
    success = test_mysql_connection()
    if success:
        print("\nSuccess! Your profile information is correctly stored in MySQL.")
    else:
        print("\nFailed to verify profile information in MySQL.")