"""
Test script for the Package Manager application
This script tests the core functionality without requiring a MySQL connection
by mocking the database interactions.
"""

import sys
import os
from unittest.mock import Mock, patch

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_database_manager():
    """Test the DatabaseManager class"""
    print("Testing DatabaseManager...")

    # Since we can't easily test the actual database connection without MySQL running,
    # we'll test the structure and basic instantiation
    from database import DatabaseManager

    # Test instantiation
    db = DatabaseManager()
    assert db.host == 'localhost'
    assert db.database == 'package_manager'
    assert db.user == 'root'
    assert db.password == ''
    assert db.port == 3306
    print("[PASS] DatabaseManager instantiation works")

    # Test with custom parameters
    db_custom = DatabaseManager(host='test-host', database='test-db',
                               user='test-user', password='test-pass', port=3307)
    assert db_custom.host == 'test-host'
    assert db_custom.database == 'test-db'
    assert db_custom.user == 'test-user'
    assert db_custom.password == 'test-pass'
    assert db_custom.port == 3307
    print("[PASS] DatabaseManager custom parameters work")

def test_package_manager_structure():
    """Test the PackageManager class structure"""
    print("\nTesting PackageManager structure...")

    from package_manager import PackageManager
    from database import DatabaseManager

    # Test instantiation with default db manager
    with patch('package_manager.DatabaseManager') as MockDBManager:
        mock_db_instance = Mock()
        MockDBManager.return_value = mock_db_instance

        pm = PackageManager()
        assert pm.db == mock_db_instance
        MockDBManager.assert_called_once()
        print("[PASS] PackageManager instantiation with default DB works")

    # Test instantiation with provided db manager
    mock_db = Mock()
    pm = PackageManager(db_manager=mock_db)
    assert pm.db == mock_db
    print("[PASS] PackageManager instantiation with provided DB works")

def test_schema():
    """Test that the schema is valid SQL"""
    print("\nTesting schema validity...")

    with open('schema.sql', 'r') as f:
        schema_content = f.read()

    # Basic checks
    assert 'CREATE DATABASE IF NOT EXISTS package_manager;' in schema_content
    assert 'CREATE TABLE IF NOT EXISTS packages' in schema_content
    assert 'CREATE TABLE IF NOT EXISTS package_installations' in schema_content
    assert 'PRIMARY KEY' in schema_content
    assert 'FOREIGN KEY' in schema_content
    print("[PASS] Schema contains required SQL statements")

def test_requirements():
    """Test that requirements.txt exists and has content"""
    print("\nTesting requirements...")

    assert os.path.exists('requirements.txt')
    with open('requirements.txt', 'r') as f:
        content = f.read().strip()

    assert len(content) > 0
    assert 'mysql-connector-python' in content
    print("[PASS] requirements.txt exists and contains mysql-connector-python")

def main():
    """Run all tests"""
    print("Running Package Manager tests...\n")

    try:
        test_database_manager()
        test_package_manager_structure()
        test_schema()
        test_requirements()

        print("\n[SUCCESS] All tests passed! The package manager structure is valid.")
        print("\nNote: Actual database functionality tests require MySQL to be running.")
        print("To test with a real database:")
        print("1. Install and start MySQL server")
        print("2. Ensure you can connect as root (or update credentials in code)")
        print("3. Run: python -c \"from database import DatabaseManager; db=DatabaseManager(); db.connect(); print('Connected!')\"")

    except Exception as e:
        print(f"\n[FAIL] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())