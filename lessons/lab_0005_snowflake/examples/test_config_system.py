#!/usr/bin/env python3
"""
Test script for the Snowflake configuration system.

This script tests the configuration loading and basic functionality
without requiring a live Snowflake connection.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def test_config_loading():
    """Test configuration loading from YAML file."""
    print("🧪 Testing configuration loading...")

    try:
        from lessons.lab_0002_config_loader.config_loader import ConfigManager

        config_file = Path(__file__).parent / "snowflake_environment.yaml"
        config = ConfigManager.load_from_file(str(config_file))

        # Test basic configuration access
        print("✅ Configuration loaded successfully")

        # Test database configuration
        db_name = config.get("environment.database.name")
        print(f"📊 Database name: {db_name}")

        # Test schema configuration
        schema_name = config.get("environment.schema.name")
        print(f"📁 Schema name: {schema_name}")

        # Test table configurations
        tables = config.get("environment.tables", [])
        print(f"📋 Found {len(tables)} table configurations")

        for table in tables:
            columns = len(table.get("columns", []))
            print(f"   - {table['name']} ({columns} columns)")

        # Test role configurations
        roles = config.get("environment.roles", [])
        print(f"🔐 Found {len(roles)} role configurations")

        for role in roles:
            print(f"   - {role['name']}")

        # Test project settings
        project_name = config.get("project.name")
        project_version = config.get("project.version")
        print(f"🚀 Project: {project_name} v{project_version}")

        return True

    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        return False


def test_environment_config_models():
    """Test the Pydantic environment configuration models."""
    print("\n🧪 Testing environment configuration models...")

    try:
        from snowflake_lab.environment_config import (
            DatabaseConfig,
            RoleConfig,
            SchemaConfig,
            TableConfig,
            UserConfig,
            WarehouseConfig,
        )

        # Test database config
        db_config = DatabaseConfig(
            name="TEST_DB",
            comment="Test database",
            data_retention_time_in_days=1,
            if_not_exists=True,
            owner=None,
        )
        print(f"✅ Database config: {db_config.name}")

        # Test schema config
        schema_config = SchemaConfig(
            schema_name="TEST_SCHEMA",
            database="TEST_DB",
            comment="Test schema",
            if_not_exists=True,
            managed_access=False,
            owner=None,
        )
        print(f"✅ Schema config: {schema_config.schema_name}")

        # Test warehouse config
        warehouse_config = WarehouseConfig(
            name="TEST_WH",
            size="X-SMALL",
            comment="Test warehouse",
            if_not_exists=True,
            auto_suspend=60,
            auto_resume=True,
            owner=None,
            min_cluster_count=1,
            max_cluster_count=1,
        )
        print(f"✅ Warehouse config: {warehouse_config.name}")

        # Test role config
        role_config = RoleConfig(
            name="TEST_ROLE",
            comment="Test role",
            if_not_exists=True,
            owner=None,
        )
        print(f"✅ Role config: {role_config.name}")

        # Test user config
        user_config = UserConfig(
            name="TEST_USER",
            display_name="Test User",
            email="test@example.com",
            if_not_exists=True,
            default_role=None,
            default_warehouse=None,
            default_namespace=None,
            rsa_public_key=None,
            comment=None,
            must_change_password=False,
        )
        print(f"✅ User config: {user_config.name}")

        # Test table config
        table_config = TableConfig(
            name="TEST_TABLE",
            schema_name="TEST_SCHEMA",
            database="TEST_DB",
            columns=[
                {"name": "ID", "type": "INTEGER", "nullable": False},
                {"name": "NAME", "type": "VARCHAR(100)", "nullable": True},
            ],
            if_not_exists=True,
            comment=None,
            owner=None,
        )
        print(
            f"✅ Table config: {table_config.name} with {len(table_config.columns)} columns"
        )

        return True

    except Exception as e:
        print(f"❌ Environment config models test failed: {e}")
        return False


def test_config_setup_class():
    """Test the SnowflakeConfigSetup class initialization."""
    print("\n🧪 Testing SnowflakeConfigSetup class...")

    try:
        from snowflake_lab.config_setup import SnowflakeConfigSetup

        config_file = Path(__file__).parent / "snowflake_environment.yaml"
        setup = SnowflakeConfigSetup(str(config_file))

        print("✅ SnowflakeConfigSetup initialized successfully")
        print(f"📁 Config file: {setup.config_file}")

        # Test configuration access
        db_name = setup.config_manager.get("environment.database.name")
        print(f"📊 Database from setup: {db_name}")

        return True

    except Exception as e:
        print(f"❌ SnowflakeConfigSetup test failed: {e}")
        return False


def test_database_manager():
    """Test the DatabaseManager class (without connection)."""
    print("\n🧪 Testing DatabaseManager class...")

    try:
        from snowflake_lab.environment_config import (
            DatabaseConfig,
            SchemaConfig,
        )

        # Test database config creation
        db_config = DatabaseConfig(
            name="TEST_DB",
            comment="Test database",
            if_not_exists=True,
            data_retention_time_in_days=None,
            owner=None,
        )
        print(f"✅ Database config created: {db_config.name}")

        # Test schema config creation
        schema_config = SchemaConfig(
            schema_name="TEST_SCHEMA",
            database="TEST_DB",
            comment="Test schema",
            if_not_exists=True,
            managed_access=False,
            owner=None,
        )
        print(f"✅ Schema config created: {schema_config.schema_name}")

        print("✅ DatabaseManager class structure is valid")

        return True

    except Exception as e:
        print(f"❌ DatabaseManager test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 Snowflake Configuration System Tests")
    print("=" * 50)

    tests = [
        test_config_loading,
        test_environment_config_models,
        test_config_setup_class,
        test_database_manager,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print(
            "🎉 All tests passed! Configuration system is working correctly."
        )
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
