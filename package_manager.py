from database import DatabaseManager
from typing import List, Dict, Optional

class PackageManager:
    def __init__(self, db_manager: DatabaseManager = None):
        self.db = db_manager or DatabaseManager()
        if not self.db.connection or not self.db.connection.is_connected():
            self.db.connect()

    def add_package(self, name: str, description: str = None) -> bool:
        """Add a new package to the system"""
        query = "INSERT INTO packages (name, description) VALUES (%s, %s)"
        result = self.db.execute_query(query, (name, description))
        return result is not None and result > 0

    def get_package(self, name: str) -> Optional[Dict]:
        """Get package information by name"""
        query = "SELECT * FROM packages WHERE name = %s"
        result = self.db.execute_query(query, (name,))
        if result and len(result) > 0:
            return result[0]
        return None

    def get_package_by_id(self, package_id: int) -> Optional[Dict]:
        """Get package information by ID"""
        query = "SELECT * FROM packages WHERE id = %s"
        result = self.db.execute_query(query, (package_id,))
        if result and len(result) > 0:
            return result[0]
        return None

    def list_packages(self) -> List[Dict]:
        """List all packages"""
        query = "SELECT * FROM packages ORDER BY name"
        result = self.db.execute_query(query)
        return result if result else []

    def install_version(self, package_name: str, version_number: str) -> bool:
        """Install a version of a package"""
        # First get the package
        package = self.get_package(package_name)
        if not package:
            # If package doesn't exist, add it
            if not self.add_package(package_name):
                return False
            package = self.get_package(package_name)

        # Check if this version is already installed
        query = """
        SELECT id FROM package_installations
        WHERE package_id = %s AND version_number = %s
        """
        result = self.db.execute_query(query, (package['id'], version_number))
        if result and len(result) > 0:
            # Version already exists, mark it as current
            return self.set_current_version(package['id'], version_number)

        # Install new version
        query = """
        INSERT INTO package_installations (package_id, version_number, is_current)
        VALUES (%s, %s, %s)
        """
        result = self.db.execute_query(query, (package['id'], version_number, True))
        if result is not None and result > 0:
            # If this was set as current, unset any other current versions
            if True:  # is_current
                self._unset_other_current_versions(package['id'], version_number)
            return True
        return False

    def set_current_version(self, package_id: int, version_number: str) -> bool:
        """Set a specific version as the current version for a package"""
        # First unset any current versions
        self._unset_other_current_versions(package_id, version_number)

        # Set the specified version as current
        query = """
        UPDATE package_installations
        SET is_current = TRUE
        WHERE package_id = %s AND version_number = %s
        """
        result = self.db.execute_query(query, (package_id, version_number))
        return result is not None and result > 0

    def _unset_other_current_versions(self, package_id: int, exclude_version: str):
        """Unset current status for all versions except the specified one"""
        query = """
        UPDATE package_installations
        SET is_current = FALSE
        WHERE package_id = %s AND version_number != %s
        """
        self.db.execute_query(query, (package_id, exclude_version))

    def get_installed_versions(self, package_name: str) -> List[Dict]:
        """Get all installed versions for a package"""
        package = self.get_package(package_name)
        if not package:
            return []

        query = """
        SELECT * FROM package_installations
        WHERE package_id = %s
        ORDER BY installed_at DESC
        """
        result = self.db.execute_query(query, (package['id'],))
        return result if result else []

    def get_installed_versions_by_id(self, package_id: int) -> List[Dict]:
        """Get all installed versions for a package by ID"""
        query = """
        SELECT * FROM package_installations
        WHERE package_id = %s
        ORDER BY installed_at DESC
        """
        result = self.db.execute_query(query, (package_id,))
        return result if result else []

    def get_current_version(self, package_name: str) -> Optional[Dict]:
        """Get the currently installed version for a package"""
        package = self.get_package(package_name)
        if not package:
            return None

        query = """
        SELECT * FROM package_installations
        WHERE package_id = %s AND is_current = TRUE
        """
        result = self.db.execute_query(query, (package['id'],))
        if result and len(result) > 0:
            return result[0]
        return None

    def remove_package(self, package_name: str) -> bool:
        """Remove a package and all its installations"""
        package = self.get_package(package_name)
        if not package:
            return False

        # Delete installations first (due to foreign key constraint)
        query = "DELETE FROM package_installations WHERE package_id = %s"
        self.db.execute_query(query, (package['id'],))

        # Delete the package
        query = "DELETE FROM packages WHERE id = %s"
        result = self.db.execute_query(query, (package['id'],))
        return result is not None and result > 0

    def remove_version(self, package_name: str, version_number: str) -> bool:
        """Remove a specific version of a package"""
        package = self.get_package(package_name)
        if not package:
            return False

        query = """
        DELETE FROM package_installations
        WHERE package_id = %s AND version_number = %s
        """
        result = self.db.execute_query(query, (package['id'], version_number))
        return result is not None and result > 0

if __name__ == "__main__":
    # Example usage
    pm = PackageManager()

    # Add a package
    print("Adding package 'example-package'...")
    if pm.add_package("example-package", "An example package"):
        print("Package added successfully")
    else:
        print("Failed to add package")

    # Install a version
    print("\nInstalling version 1.0.0...")
    if pm.install_version("example-package", "1.0.0"):
        print("Version installed successfully")
    else:
        print("Failed to install version")

    # Install another version
    print("\nInstalling version 2.0.0...")
    if pm.install_version("example-package", "2.0.0"):
        print("Version installed successfully")
    else:
        print("Failed to install version")

    # Set current version
    print("\nSetting version 1.0.0 as current...")
    package = pm.get_package("example-package")
    if package:
        if pm.set_current_version(package['id'], "1.0.0"):
            print("Current version set successfully")
        else:
            print("Failed to set current version")
    else:
        print("Package not found")

    # List packages
    print("\nListing all packages:")
    packages = pm.list_packages()
    for pkg in packages:
        print(f"- {pkg['name']}: {pkg['description']}")

    # Get installed versions
    print("\nInstalled versions for 'example-package':")
    versions = pm.get_installed_versions("example-package")
    for ver in versions:
        current = " (current)" if ver['is_current'] else ""
        print(f"- {ver['version_number']}{current} (installed {ver['installed_at']})")

    # Get current version
    current = pm.get_current_version("example-package")
    if current:
        print(f"\nCurrent version: {current['version_number']}")