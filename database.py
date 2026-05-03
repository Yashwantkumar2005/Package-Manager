import mysql.connector
from mysql.connector import Error
import os
from contextlib import contextmanager

class DatabaseManager:
    def __init__(self, host='localhost', database='',
                 user='root', password='', port=3306):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    def connect(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port,
                autocommit=False  # Disable autocommit for explicit transaction control
            )
            if self.connection.is_connected():
                print(f"Connected to MySQL database '{self.database}'")
                return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")

    def is_connected(self):
        """Check if database connection is active"""
        return self.connection is not None and self.connection.is_connected()

    @contextmanager
    def get_cursor(self):
        """Context manager for database cursor"""
        if not self.connection or not self.connection.is_connected():
            if not self.connect():
                raise Exception("Failed to connect to database")

        cursor = self.connection.cursor(dictionary=True)
        try:
            yield cursor
        finally:
            cursor.close()

    @contextmanager
    def transaction(self):
        """Context manager for database transactions"""
        if not self.connection or not self.connection.is_connected():
            if not self.connect():
                raise Exception("Failed to connect to database")

        try:
            yield
            self.connection.commit()
        except Error as e:
            self.connection.rollback()
            raise e

    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params or ())
                if cursor.with_rows:
                    result = cursor.fetchall()
                    return result
                else:
                    self.connection.commit()
                    return cursor.rowcount
        except Error as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
            return None

# Convenience functions for package manager operations
def get_db_connection():
    """Get a database connection instance"""
    # You can customize these parameters or read from environment variables
    db = DatabaseManager(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', ''),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        port=int(os.getenv('DB_PORT', 3306))
    )
    if db.connect():
        return db
    return None

if __name__ == "__main__":
    # Test the connection
    db = get_db_connection()
    if db:
        # Test query
        result = db.execute_query("SELECT DATABASE()")
        print(f"Current database: {result}")
        db.disconnect()