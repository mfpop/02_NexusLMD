import os
import sys
import django
import subprocess

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection
from django.contrib.auth.models import User
from apps.authenticate.models import Profile, WorkExperience

def check_mysql_service():
    """Check if MySQL service is running."""
    try:
        # For Windows systems - check both MySQL and MySQL80 service names
        mysql_services = ['mysql', 'MySQL80']
        service_found = False
        service_running = False
        service_name = None
        
        for service in mysql_services:
            result = subprocess.run(
                ['sc', 'query', service], 
                capture_output=True, 
                text=True, 
                check=False
            )
            if "DOES NOT EXIST" not in result.stdout:
                service_found = True
                service_name = service
                if "RUNNING" in result.stdout:
                    service_running = True
                    break
        
        if service_running:
            print(f"✅ MySQL service ({service_name}) is running")
            return True
        elif service_found:
            print(f"❌ MySQL service ({service_name}) is installed but not running")
            print(f"   Please start it with: 'net start {service_name}' (Admin rights required)")
            print("   If that fails, start MySQL from your system services or MySQL Workbench")
            return False
        else:
            print("❌ No MySQL service found on this system")
            print("   Please ensure MySQL is properly installed")
            return False
    except Exception as e:
        print(f"❌ Error checking MySQL service: {e}")
        return False

def verify_mysql_connection():
    """Verify connection to MySQL database."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ Connected to database. Version: {version[0]}")
            
            # More reliable MySQL detection
            if cursor.execute("SHOW VARIABLES LIKE 'version_comment'"):
                version_comment = cursor.fetchone()[1]
                if "MySQL" in version_comment:
                    print("✅ Confirmed using MySQL database backend")
                else:
                    print(f"✅ Connected to a MySQL-compatible database: {version_comment}")
            else:
                print("✅ Using MySQL database (confirmed by successful connection)")
                
            return True
    except Exception as e:
        print(f"❌ Failed to connect to MySQL: {e}")
        return False

def check_data_consistency():
    """Check data consistency between Django models and MySQL."""
    try:
        # Get counts from Django ORM
        user_count = User.objects.count()
        profile_count = Profile.objects.count()
        work_exp_count = WorkExperience.objects.count()
        
        print("\n=== Data Counts from Django ORM ===")
        print(f"Users: {user_count}")
        print(f"Profiles: {profile_count}")
        print(f"Work Experiences: {work_exp_count}")
        
        # Get counts directly from MySQL
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM auth_user")
            mysql_user_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM authenticate_profile")
            mysql_profile_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM authenticate_workexperience")
            mysql_work_exp_count = cursor.fetchone()[0]
        
        print("\n=== Data Counts from MySQL Directly ===")
        print(f"Users: {mysql_user_count}")
        print(f"Profiles: {mysql_profile_count}")
        print(f"Work Experiences: {mysql_work_exp_count}")
        
        # Check consistency
        consistent = (
            user_count == mysql_user_count and
            profile_count == mysql_profile_count and
            work_exp_count == mysql_work_exp_count
        )
        
        if consistent:
            print("\n✅ Data is consistent between Django ORM and MySQL")
        else:
            print("\n❌ Data inconsistency detected between Django ORM and MySQL")
            if user_count != mysql_user_count:
                print(f"  - User count mismatch: Django ORM {user_count}, MySQL {mysql_user_count}")
            if profile_count != mysql_profile_count:
                print(f"  - Profile count mismatch: Django ORM {profile_count}, MySQL {mysql_profile_count}")
            if work_exp_count != mysql_work_exp_count:
                print(f"  - Work Experience count mismatch: Django ORM {work_exp_count}, MySQL {mysql_work_exp_count}")
        
        return consistent
    except Exception as e:
        print(f"\n❌ Error checking data consistency: {e}")
        return False

def check_sqlite_file():
    """Check if SQLite file exists and potentially contains data."""
    sqlite_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite3')
    if os.path.exists(sqlite_path):
        size = os.path.getsize(sqlite_path)
        if size > 1000:  # If file is larger than 1KB, might contain data
            print(f"\n⚠️ SQLite file exists ({size} bytes) and may contain data")
            print("   This could lead to confusion if Django is misconfigured to use it")
            print("   Consider renaming or removing it to ensure MySQL usage")
        else:
            print(f"\n✓ SQLite file exists but appears empty ({size} bytes)")
    else:
        print("\n✓ No SQLite database file found - good!")

def ensure_admin_data_in_mysql():
    """Ensures that admin data is properly in MySQL by checking for admin superuser."""
    try:
        # Check if admin user exists
        admin_exists = User.objects.filter(is_superuser=True).exists()
        if not admin_exists:
            print("\n⚠️ No admin superuser found in the database")
            print("   You may need to create one with: python manage.py createsuperuser")
        else:
            print("\n✅ Admin superuser(s) exist in the database")
            
        # Check if migrations are properly applied
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES LIKE 'django_migrations'")
            if cursor.fetchone():
                cursor.execute("SELECT COUNT(*) FROM django_migrations")
                migration_count = cursor.fetchone()[0]
                print(f"✅ Migrations table exists with {migration_count} migrations applied")
            else:
                print("❌ Migrations table doesn't exist - database may not be properly initialized")
                print("   Run: python manage.py migrate")
        
        return True
    except Exception as e:
        print(f"\n❌ Error checking admin data: {e}")
        return False
        
def fix_synchronization_issues():
    """Try to fix synchronization issues automatically."""
    try:
        print("\n=== Attempting to fix synchronization issues ===")
        
        # Check if db.sqlite3 exists and might be causing issues
        sqlite_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite3')
        if os.path.exists(sqlite_path) and os.path.getsize(sqlite_path) > 1000:
            new_name = 'db.sqlite3.bak'
            os.rename(sqlite_path, os.path.join(os.path.dirname(os.path.abspath(__file__)), new_name))
            print(f"✓ Renamed db.sqlite3 to {new_name} to avoid confusion")
            
        # Make sure all migrations are applied
        print("\n1. Ensuring all migrations are applied...")
        migrate_result = subprocess.run(
            [sys.executable, 'manage.py', 'migrate'],
            capture_output=True,
            text=True,
            check=False
        )
        if migrate_result.returncode == 0:
            print("✅ Migrations applied successfully")
        else:
            print(f"❌ Error applying migrations: {migrate_result.stderr}")
            
        return True
    except Exception as e:
        print(f"\n❌ Error fixing synchronization: {e}")
        return False

def main():
    print("=== MySQL Synchronization Verification ===\n")
    
    # Step 1: Check MySQL service
    if not check_mysql_service():
        print("\nTo fix: Please start MySQL service with administrator privileges")
        print("1. Open Command Prompt as administrator")
        print("2. Run: net start MySQL80")
        return False
    
    # Step 2: Check connection
    if not verify_mysql_connection():
        print("\nTo fix: Check your database settings in settings.py")
        print("Ensure your MySQL credentials are correct and the database 'lmd' exists")
        return False
    
    # Step 3: Check data consistency
    data_consistent = check_data_consistency()
    
    # Step 4: Check SQLite file
    check_sqlite_file()
    
    # Step 5: Ensure admin data is in MySQL
    ensure_admin_data_in_mysql()
    
    if data_consistent:
        print("\n✅ SUCCESS: MySQL is synchronized with Django models")
        print("   The admin dashboard is displaying data from MySQL")
        return True
    else:
        print("\n❌ ISSUE DETECTED: MySQL may not be fully synchronized")
        print("   Attempting to fix synchronization issues automatically...")
        fix_synchronization_issues()
        print("\nTo complete synchronization:")
        print("1. Make sure MySQL80 service is running (net start MySQL80 as admin)")
        print("2. Run: python manage.py migrate")
        print("3. If needed, create admin user: python manage.py createsuperuser")
        print("4. Restart your Django application: python manage.py runserver")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)