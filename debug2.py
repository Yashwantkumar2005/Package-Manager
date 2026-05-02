import os

# Set environment variables
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_USER'] = 'root'
os.environ['DB_NAME'] = 'package_manager'
os.environ['DB_PASSWORD'] = 'test123'
os.environ['DB_PORT'] = '3306'

# Now simulate what get_db_connection does
host = os.getenv('DB_HOST', 'localhost')
database = os.getenv('DB_NAME', 'package_manager')
user = os.getenv('DB_USER', 'root')
password = os.getenv('DB_PASSWORD', '')
port = int(os.getenv('DB_PORT', 3306))

print("Values to be passed to DatabaseManager:")
print(f"  host: {repr(host)}")
print(f"  database: {repr(database)}")
print(f"  user: {repr(user)}")
print(f"  password: {repr(password)}")
print(f"  port: {repr(port)}")

# Now create DatabaseManager
from database import DatabaseManager
db = DatabaseManager(host=host, database=database, user=user, password=password, port=port)

print("\nDatabaseManager instance variables:")
print(f"  host: {repr(db.host)}")
print(f"  database: {repr(db.database)}")
print(f"  user: {repr(db.user)}")
print(f"  password: {repr(db.password)}")
print(f"  port: {repr(db.port)}")

print("\nAttempting to connect...")
if db.connect():
    print("SUCCESS: Connected to database!")
    # Test a query
    result = db.execute_query("SELECT DATABASE()")
    print(f"Current database: {result}")
    db.disconnect()
else:
    print("FAILED: Could not connect to database")
