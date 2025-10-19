#!/usr/bin/env python3
"""Test script to verify Snowflake connection setup.

This script tests the Snowflake connection using the configuration
from your .env file and displays connection information.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import after path modification
from lessons.lab_0005_snowflake.snowflake_lab import (  # noqa: E402
    SnowflakeConnection,
    SnowparkOperations,
)


def test_connection():
    """Test the Snowflake connection and display information."""
    print("🔗 Testing Snowflake Connection...")
    print("=" * 50)

    connection = None
    try:
        # Create connection from environment variables
        print("📋 Loading configuration from .env file...")
        connection = SnowflakeConnection.from_environment()

        # Test basic connection
        print("🔍 Testing connection...")
        if connection.test_connection():
            print("✅ Connection successful!")
        else:
            print("❌ Connection failed!")
            return False

        # Get connection information
        print("\n📊 Connection Information:")
        print("-" * 30)
        info = connection.get_connection_info()

        if "error" in info:
            print(f"❌ Error getting connection info: {info['error']}")
            return False

        print(f"Account: {info['account']}")
        print(f"User: {info['user']}")
        print(f"Warehouse: {info['warehouse']}")
        print(f"Database: {info['database']}")
        print(f"Schema: {info['schema']}")
        print(f"Role: {info['role']}")
        print(f"Active Sessions: {info['active_sessions']}")

        # Test Snowpark operations
        print("\n🔧 Testing Snowpark Operations...")
        print("-" * 30)

        with connection.session_context() as session:
            ops = SnowparkOperations(session)

            # Test a simple query
            print(
                "Running test query: SELECT 1 as test_value, CURRENT_TIMESTAMP() as current_time"
            )
            df = ops.read_sql(
                "SELECT 1 as test_value, CURRENT_TIMESTAMP() as current_time"
            )
            result = ops.collect_data(df)

            if result:
                print("✅ Query executed successfully!")
                print(f"Test Value: {result[0]['TEST_VALUE']}")
                print(f"Current Time: {result[0]['CURRENT_TIME']}")
            else:
                print("❌ Query returned no results")
                return False

        print(
            "\n🎉 All tests passed! Your Snowflake setup is working correctly."
        )
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print(
            "1. Make sure your .env file exists and contains valid Snowflake credentials"
        )
        print("2. Verify your private key file exists and is accessible")
        print(
            "3. Check that the user MS3DM_LOCAL_DEV has been created in Snowflake"
        )
        print("4. Ensure your account identifier is correct")
        print(
            "5. Run the setup_snowflake_user.sql script if you haven't already"
        )
        return False

    finally:
        # Clean up connections
        if connection:
            try:
                connection.close_all_sessions()
            except Exception:
                pass


def main():
    """Main function."""
    print("❄️  Snowflake Lab - Connection Test")
    print("=" * 50)

    # Check if .env file exists
    env_file = project_root / ".env"
    if not env_file.exists():
        print("❌ .env file not found!")
        print(f"Please create a .env file in {project_root}")
        print("You can use the template: examples/snowflake.env.template")
        return False

    success = test_connection()

    if success:
        print("\n🚀 Ready to start using Snowflake Lab!")
        print("Try running: python examples/basic_operations.py")
    else:
        print("\n💡 Need help? Check the README.md for setup instructions")

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
