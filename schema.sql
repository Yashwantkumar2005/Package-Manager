-- Database schema for Package Manager
-- Creates database and tables for tracking packages and their version history

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS package_manager;
USE package_manager;

-- Packages table stores basic package information
CREATE TABLE IF NOT EXISTS packages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Package installations table tracks version history and installation status
CREATE TABLE IF NOT EXISTS package_installations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    package_id INT NOT NULL,
    version_number VARCHAR(50) NOT NULL,
    installed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_current BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (package_id) REFERENCES packages(id) ON DELETE CASCADE,
    -- Ensure only one current version per package
    UNIQUE KEY unique_current_version (package_id, is_current) WHERE (is_current = TRUE)
);

-- Index for faster lookups
CREATE INDEX idx_package_id ON package_installations(package_id);
CREATE INDEX idx_installed_at ON package_installations(installed_at);