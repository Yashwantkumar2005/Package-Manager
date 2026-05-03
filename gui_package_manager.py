import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from package_manager import PackageManager
import os
import re

class PackageManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Package Manager")
        self.root.geometry("800x600")

        # Set environment variables for database connection
        # NOTE: Users should override these with their own credentials when running the application
        # Example: DB_HOST=localhost DB_USER=myuser DB_PASSWORD=mypass DB_NAME=package_manager DB_PORT=3306 python gui_package_manager.py
        if not os.environ.get('DB_HOST'):
            os.environ['DB_HOST'] = 'localhost'
        if not os.environ.get('DB_USER'):
            os.environ['DB_USER'] = 'root'
        if not os.environ.get('DB_PASSWORD'):
            os.environ['DB_PASSWORD'] = ''  # Empty default - users should set their own
        if not os.environ.get('DB_NAME'):
            os.environ['DB_NAME'] = ''      # Empty default - users should set their own
        if not os.environ.get('DB_PORT'):
            os.environ['DB_PORT'] = '3306'

        # Initialize package manager
        try:
            self.pm = PackageManager()
            self.status_var = tk.StringVar()
            self.status_var.set("Ready")
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {str(e)}")
            self.pm = None

        self.create_widgets()
        if self.pm:
            self.refresh_package_list()

    def _validate_package_name(self, name):
        """Validate package name - matches the validation in PackageManager"""
        if not name or not isinstance(name, str):
            return False
        if len(name) > 255:  # Match VARCHAR(255) in database
            return False
        # Allow alphanumeric, dots, hyphens, underscores; must start with alphanumeric
        return bool(re.match(r'^[a-zA-Z0-9][a-zA-Z0-9._-]*$', name))

    def _validate_version_number(self, version):
        """Validate version number - matches the validation in PackageManager"""
        if not version or not isinstance(version, str):
            return False
        if len(version) > 50:  # Match VARCHAR(50) in database
            return False
        # Allow alphanumeric, dots, hyphens, underscores
        return bool(re.match(r'^[a-zA-Z0-9._-]+$', version))

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="Package Manager", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Left panel - Package list
        left_frame = ttk.LabelFrame(main_frame, text="Packages", padding="10")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)

        # Package treeview
        self.package_tree = ttk.Treeview(left_frame, columns=("Description",), show="tree headings")
        self.package_tree.heading("#0", text="Package Name")
        self.package_tree.heading("Description", text="Description")
        self.package_tree.column("#0", width=200)
        self.package_tree.column("Description", width=300)
        self.package_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Scrollbar for package tree
        package_scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.package_tree.yview)
        package_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.package_tree.configure(yscrollcommand=package_scrollbar.set)

        # Bind package selection
        self.package_tree.bind('<<TreeviewSelect>>', self.on_package_select)

        # Button frame for package operations
        pkg_btn_frame = ttk.Frame(left_frame)
        pkg_btn_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky=(tk.W, tk.E))

        ttk.Button(pkg_btn_frame, text="Add Package", command=self.add_package).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(pkg_btn_frame, text="Remove Package", command=self.remove_package).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(pkg_btn_frame, text="Refresh", command=self.refresh_package_list).pack(side=tk.LEFT)

        # Right panel - Version management
        right_frame = ttk.LabelFrame(main_frame, text="Version Management", padding="10")
        right_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)

        # Current package info
        self.current_package_label = ttk.Label(right_frame, text="Select a package", font=("Arial", 10, "bold"))
        self.current_package_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))

        # Version treeview
        self.version_tree = ttk.Treeview(right_frame, columns=("Installed At", "Current"), show="tree headings")
        self.version_tree.heading("#0", text="Version Number")
        self.version_tree.heading("Installed At", text="Installed At")
        self.version_tree.heading("Current", text="Current")
        self.version_tree.column("#0", width=150)
        self.version_tree.column("Installed At", width=150)
        self.version_tree.column("Current", width=80)
        self.version_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Scrollbar for version tree
        version_scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.version_tree.yview)
        version_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.version_tree.configure(yscrollcommand=version_scrollbar.set)

        # Button frame for version operations
        ver_btn_frame = ttk.Frame(right_frame)
        ver_btn_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky=(tk.W, tk.E))

        ttk.Button(ver_btn_frame, text="Install Version", command=self.install_version).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(ver_btn_frame, text="Set as Current", command=self.set_current_version).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(ver_btn_frame, text="Remove Version", command=self.remove_version).pack(side=tk.LEFT, padx=(0, 5))

        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        status_frame.columnconfigure(0, weight=1)

        ttk.Label(status_frame, textvariable=self.status_var).grid(row=0, column=0, sticky=tk.W)

    def set_status(self, message):
        self.status_var.set(message)
        self.root.update_idletasks()

    def refresh_package_list(self):
        if not self.pm:
            return

        # Clear existing items
        for item in self.package_tree.get_children():
            self.package_tree.delete(item)

        # Get packages and populate tree
        packages = self.pm.list_packages()
        for pkg in packages:
            self.package_tree.insert("", tk.END, text=pkg['name'], values=(pkg['description'] or "",), tags=(str(pkg['id']),))

        self.set_status(f"Loaded {len(packages)} packages")

    def on_package_select(self, event):
        selection = self.package_tree.selection()
        if not selection:
            self.current_package_label.config(text="Select a package")
            # Clear version tree
            for item in self.version_tree.get_children():
                self.version_tree.delete(item)
            return

        item = selection[0]
        package_name = self.package_tree.item(item, "text")
        package_id = self.package_tree.item(item, "tags")[0] if self.package_tree.item(item, "tags") else None

        self.current_package_label.config(text=f"Package: {package_name}")

        # Clear and populate version tree
        for item in self.version_tree.get_children():
            self.version_tree.delete(item)

        if package_id:
            versions = self.pm.get_installed_versions_by_id(int(package_id))
            for ver in versions:
                current_text = "Yes" if ver['is_current'] else "No"
                self.version_tree.insert("", tk.END, text=ver['version_number'],
                                       values=(ver['installed_at'].strftime("%Y-%m-%d %H:%M:%S") if ver['installed_at'] else "", current_text),
                                       tags=(str(ver['id']),))

    def get_selected_package_info(self):
        selection = self.package_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Required", "Please select a package first")
            return None, None

        item = selection[0]
        package_name = self.package_tree.item(item, "text")
        package_id = self.package_tree.item(item, "tags")[0] if self.package_tree.item(item, "tags") else None

        return package_name, int(package_id) if package_id else None

    def get_selected_version_info(self):
        selection = self.version_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Required", "Please select a version first")
            return None, None

        item = selection[0]
        version_number = self.version_tree.item(item, "text")
        version_id = self.version_tree.item(item, "tags")[0] if self.version_tree.item(item, "tags") else None

        return version_number, int(version_id) if version_id else None

    def add_package(self):
        if not self.pm:
            messagebox.showerror("Error", "Package manager not initialized")
            return

        name = simpledialog.askstring("Add Package", "Enter package name:")
        if not name:
            return

        if not self._validate_package_name(name):
            messagebox.showerror("Invalid Input", f"Package name '{name}' is invalid. \n\nRules:\n- Must start with a letter or number\n- Can contain letters, numbers, dots, hyphens, and underscores\n- Maximum 255 characters")
            return

        description = simpledialog.askstring("Add Package", "Enter package description (optional):")

        if self.pm.add_package(name, description):
            messagebox.showinfo("Success", f"Package '{name}' added successfully")
            self.refresh_package_list()
        else:
            messagebox.showerror("Error", f"Failed to add package '{name}'")

    def remove_package(self):
        if not self.pm:
            messagebox.showerror("Error", "Package manager not initialized")
            return

        package_name, package_id = self.get_selected_package_info()
        if not package_name:
            return

        if messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove package '{package_name}' and all its versions?"):
            if self.pm.remove_package(package_name):
                messagebox.showinfo("Success", f"Package '{package_name}' removed successfully")
                self.refresh_package_list()
                self.current_package_label.config(text="Select a package")
                # Clear version tree
                for item in self.version_tree.get_children():
                    self.version_tree.delete(item)
            else:
                messagebox.showerror("Error", f"Failed to remove package '{package_name}'")

    def install_version(self):
        if not self.pm:
            messagebox.showerror("Error", "Package manager not initialized")
            return

        package_name, package_id = self.get_selected_package_info()
        if not package_name:
            return

        version_number = simpledialog.askstring("Install Version", f"Enter version number for '{package_name}':")
        if not version_number:
            return

        if self.pm.install_version(package_name, version_number):
            messagebox.showinfo("Success", f"Version '{version_number}' installed successfully for '{package_name}'")
            self.on_package_select(None)  # Refresh version list
        else:
            messagebox.showerror("Error", f"Failed to install version '{version_number}' for '{package_name}'")

    def set_current_version(self):
        if not self.pm:
            messagebox.showerror("Error", "Package manager not initialized")
            return

        package_name, package_id = self.get_selected_package_info()
        if not package_name:
            return

        version_number, version_id = self.get_selected_version_info()
        if not version_number:
            return

        if self.pm.set_current_version(package_id, version_number):
            messagebox.showinfo("Success", f"Version '{version_number}' set as current for '{package_name}'")
            self.on_package_select(None)  # Refresh version list
        else:
            messagebox.showerror("Error", f"Failed to set version '{version_number}' as current for '{package_name}'")

    def remove_version(self):
        if not self.pm:
            messagebox.showerror("Error", "Package manager not initialized")
            return

        package_name, package_id = self.get_selected_package_info()
        if not package_name:
            return

        version_number, version_id = self.get_selected_version_info()
        if not version_number:
            return

        if messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove version '{version_number}' of package '{package_name}'?"):
            if self.pm.remove_version(package_name, version_number):
                messagebox.showinfo("Success", f"Version '{version_number}' removed successfully from '{package_name}'")
                self.on_package_select(None)  # Refresh version list
            else:
                messagebox.showerror("Error", f"Failed to remove version '{version_number}' from '{package_name}'")

def main():
    root = tk.Tk()
    app = PackageManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()