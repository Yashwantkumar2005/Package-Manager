# Package Manager

A desktop application for managing software packages and their versions, built with Python, Tkinter, and MySQL.

## Features

- **Package Management**: Add, remove, and list packages
- **Version Control**: Install multiple versions of packages, set current versions, and remove specific versions
- **Version History**: Track installation timestamps and maintain a history of all versions
- **Current Version Tracking**: Only one version can be marked as current per package
- **MySQL Persistence**: All data stored in a MySQL database for reliability
- **Modern Tkinter GUI**: Clean, intuitive interface for easy package management

## Project Structure

```
.
├── database.py           # Database connection and query handling
├── package_manager.py    # Core package management logic
├── gui_package_manager.py # Tkinter GUI interface
├── schema.sql            # Database schema definition
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Installation

### Prerequisites

- Python 3.6+
- MySQL Server 8.0+
- mysql-connector-python package

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Yashwantkumar2005/Package-Manager.git
   cd Package-manager
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure MySQL**
   - Ensure MySQL server is running
   - The application will automatically create the `package_manager` database and tables on first launch

4. **Initialize the database**
   ```bash
   # The application will run the schema.sql automatically on first launch
   # Or you can manually initialize:
   mysql -u root -p < schema.sql
   ```

---

## Required: Configure Your Database Credentials

**The application will not launch until you fill in your database credentials.** The source files ship with blank credential fields — you must update them manually before running.

You need to edit **two files**:

---

### 1. `database.py` — Lines 7–14 and Lines 91–96

Open `database.py` and fill in your MySQL credentials in **both** locations:

**Lines 7–14** (default connection config):
```python
DB_HOST = ""       # e.g. "localhost"
DB_USER = ""       # e.g. "root"
DB_PASSWORD = ""   # e.g. "yourpassword"
DB_NAME = ""       # e.g. "package_manager"
DB_PORT =          # e.g. 3306
```

**Lines 91–96** (fallback/secondary connection config):
```python
host = ""          # e.g. "localhost"
user = ""          # e.g. "root"
password = ""      # e.g. "yourpassword"
database = ""      # e.g. "package_manager"
port =             # e.g. 3306
```

Replace the blank strings and missing values with your actual MySQL credentials.

---

### 2. `gui_package_manager.py` — Lines 16–26

Open `gui_package_manager.py` and fill in your credentials here as well:

```python
DB_HOST = ""       # e.g. "localhost"
DB_USER = ""       # e.g. "root"
DB_PASSWORD = ""   # e.g. "yourpassword"
DB_NAME = ""       # e.g. "package_manager"
DB_PORT =          # e.g. 3306
```

> **Note:** These values must match what you entered in `database.py`. The GUI reads from this file to establish its own connection to MySQL.

---

## Usage

### Running the Application

Once credentials are configured in both files, launch the app:

```bash
python gui_package_manager.py
```

Alternatively, you can pass credentials as environment variables instead of editing the files:

```bash
DB_HOST=localhost DB_USER=your_username DB_PASSWORD=your_password DB_NAME=package_manager DB_PORT=3306 python gui_package_manager.py
```

> **Note:** Since this runs on your local machine, you're using your own MySQL instance. Your packages are stored in your local database, not in any shared or remote repository.

### Using the GUI

1. **Add a Package**
   - Click "Add Package" button
   - Enter package name and optional description

2. **Install Versions**
   - Select a package from the list
   - Click "Install Version"
   - Enter the version number to install

3. **Set Current Version**
   - Select a package
   - Select a version from the version list
   - Click "Set as Current"

4. **Remove Versions/Packages**
   - Select the item to remove
   - Click the appropriate remove button
   - Confirm the action in the dialog

5. **Refresh**
   - Click "Refresh" to reload the package list from the database

## Database Schema

The application uses two tables:

### packages
- `id`: Auto-increment primary key
- `name`: Unique package name
- `description`: Package description
- `created_at`: Timestamp of package creation

### package_installations
- `id`: Auto-increment primary key
- `package_id`: Foreign key to packages table
- `version_number`: Version string (e.g., "1.0.0")
- `installed_at`: Timestamp of installation
- `is_current`: Boolean flag indicating if this is the current version

## Configuration Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `DB_HOST` | MySQL server host | `localhost` |
| `DB_USER` | MySQL username | `root` |
| `DB_PASSWORD` | MySQL password | `yourpassword` |
| `DB_NAME` | Database name | `package_manager` |
| `DB_PORT` | MySQL port | `3306` |

These must be set in both `database.py` (lines 7–14 and 91–96) and `gui_package_manager.py` (lines 16–26).