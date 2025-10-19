#!/usr/bin/env python3
"""
Snowflake Environment Setup Script

This script sets up a complete Snowflake environment based on configuration files.
It uses the lab_0002 config loader to manage all configuration.

Usage:
    python setup_environment.py [config_file]

If no config_file is provided, it will use 'snowflake_environment.yaml' in the same directory.
"""

import logging
import sys
from pathlib import Path

from snowflake_lab.config_setup import SnowflakeConfigSetup

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("snowflake_setup.log"),
    ],
)

logger = logging.getLogger(__name__)


def setup_environment(config_file: str | None = None) -> bool:  # noqa: C901
    """
    Set up the Snowflake environment based on configuration.

    Args:
        config_file: Path to configuration file

    Returns:
        True if setup successful, False otherwise
    """
    if not config_file:
        config_file_path = Path(__file__).parent / "snowflake_environment.yaml"
    else:
        config_file_path = Path(config_file)

    config_path = config_file_path
    if not config_path.exists():
        logger.error(f"Configuration file not found: {config_path}")
        return False

    logger.info(f"Setting up Snowflake environment using: {config_path}")

    try:
        # Initialize the config setup
        setup = SnowflakeConfigSetup(str(config_path))

        # Set up the environment
        results = setup.setup_environment()

        # Print results
        print("\n" + "=" * 60)
        print("❄️  SNOWFLAKE ENVIRONMENT SETUP RESULTS")
        print("=" * 60)

        if "error" in results:
            print(f"❌ Setup failed: {results['error']}")
            return False

        # Connection
        if results.get("connection"):
            print("✅ Connection: Successfully connected to Snowflake")
        else:
            print("❌ Connection: Failed to connect to Snowflake")
            return False

        # Database
        if "database" in results:
            if results["database"]:
                print("✅ Database: Successfully created/verified database")
            else:
                print("❌ Database: Failed to create database")

        # Schema
        if "schema" in results:
            if results["schema"]:
                print("✅ Schema: Successfully created/verified schema")
            else:
                print("❌ Schema: Failed to create schema")

        # Warehouse
        if "warehouse" in results:
            if results["warehouse"]:
                print("✅ Warehouse: Successfully created/verified warehouse")
            else:
                print("❌ Warehouse: Failed to create warehouse")

        # Roles
        if "roles" in results:
            role_results = results["roles"]
            print(
                f"🔐 Roles: {sum(role_results.values())}/{len(role_results)} created successfully"
            )
            for role_name, success in role_results.items():
                status = "✅" if success else "❌"
                print(f"   {status} {role_name}")

        # Users
        if "users" in results:
            user_results = results["users"]
            print(
                f"👤 Users: {sum(user_results.values())}/{len(user_results)} created successfully"
            )
            for user_name, success in user_results.items():
                status = "✅" if success else "❌"
                print(f"   {status} {user_name}")

        # Tables
        if "tables" in results:
            table_results = results["tables"]
            print(
                f"📊 Tables: {sum(table_results.values())}/{len(table_results)} created successfully"
            )
            for table_name, success in table_results.items():
                status = "✅" if success else "❌"
                print(f"   {status} {table_name}")

        # Grants
        if "grants" in results:
            grant_results = results["grants"]
            print(
                f"🔑 Grants: {sum(grant_results.values())}/{len(grant_results)} executed successfully"
            )

        print("\n" + "=" * 60)
        print("🎉 SNOWFLAKE ENVIRONMENT SETUP COMPLETE!")
        print("=" * 60)

        # Close the connection
        setup.close()

        return True

    except Exception as e:
        logger.error(f"Setup failed with error: {e}")
        print(f"\n❌ Setup failed: {e}")
        return False


def verify_environment(config_file: str | None = None) -> bool:
    """
    Verify the Snowflake environment setup.

    Args:
        config_file: Path to configuration file

    Returns:
        True if verification successful, False otherwise
    """
    if not config_file:
        config_file_path = Path(__file__).parent / "snowflake_environment.yaml"
    else:
        config_file_path = Path(config_file)

    try:
        setup = SnowflakeConfigSetup(str(config_file_path))

        if not setup.connect():
            print("❌ Failed to connect to Snowflake")
            return False

        print("\n🔍 VERIFYING SNOWFLAKE ENVIRONMENT")
        print("=" * 40)

        # Check database
        db_manager = setup.db_manager
        if db_manager:
            databases = db_manager.list_databases()
            python_lab_db = any(
                db.get("name") == "PYTHON_LEARNING_LAB" for db in databases
            )
            print(
                f"📊 Database PYTHON_LEARNING_LAB: {'✅ Found' if python_lab_db else '❌ Not found'}"
            )

            if python_lab_db:
                schemas = db_manager.list_schemas("PYTHON_LEARNING_LAB")
                examples_schema = any(
                    schema.get("name") == "EXAMPLES" for schema in schemas
                )
                print(
                    f"📁 Schema EXAMPLES: {'✅ Found' if examples_schema else '❌ Not found'}"
                )

        # Test a simple query
        try:
            if setup.session:
                result = setup.session.sql(
                    "SELECT CURRENT_VERSION() as version"
                ).collect()
            else:
                print("🔗 Connection test: ❌ No session available")
                return False
            if result:
                print(
                    f"🔗 Connection test: ✅ Snowflake version {result[0]['VERSION']}"
                )
        except Exception as e:
            print(f"🔗 Connection test: ❌ {e}")

        setup.close()
        return True

    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Set up Snowflake environment"
    )
    parser.add_argument(
        "config_file",
        nargs="?",
        help="Path to configuration file (default: snowflake_environment.yaml)",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Only verify the environment, don't set it up",
    )

    args = parser.parse_args()

    if args.verify_only:
        success = verify_environment(args.config_file)
    else:
        success = setup_environment(args.config_file)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
