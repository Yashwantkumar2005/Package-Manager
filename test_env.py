import os

# Set environment variables
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_USER'] = 'root'
os.environ['DB_NAME'] = 'package_manager'
os.environ['DB_PASSWORD'] = 'test123'
os.environ['DB_PORT'] = '3306'

print("Environment variables:")
print(f"  DB_HOST: {repr(os.getenv('DB_HOST'))}")
print(f"  DB_USER: {repr(os.getenv('DB_USER'))}")
print(f"  DB_NAME: {repr(os.getenv('DB_NAME'))}")
print(f"  DB_PASSWORD: {repr(os.getenv('DB_PASSWORD'))}")
print(f"  DB_PORT: {repr(os.getenv('DB_PORT'))}")

# Now test what gets passed to DatabaseManager
host = os.getenv('DB_HOST', 'localhost')
database = os.getenv('DB_NAME', 'package_manager')
user = os.getenv('DB_USER', 'root')
password = os.getenv('DB_PASSWORD', '')
port = int(os.getenv('DB_PORT', 3306))

print("\nValues to be passed:")
print(f"  host: {repr(host)}")
print(f"  database: {repr(database)}")
print(f"  user: {repr(user)}")
print(f"  password: {repr(password)}")
print(f"  port: {repr(port)}")

# Test DatabaseManager
from database import DatabaseManager
db = DatabaseManager(host=host, database=database, user=user, password=password, port=port)
print("\nDatabaseManager values:")
print(f"  host: {repr(db.host)}")
print(f"  database: {repr(db.database)}")
print(f"  user: {repr(db.user)}")
print(f"  password: {repr(db.password)}")
print(f"  port: {repr(db.port)}")
