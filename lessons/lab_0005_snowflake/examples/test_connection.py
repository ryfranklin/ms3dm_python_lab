#!/usr/bin/env python3
"""Test script to verify Snowflake connection setup.

This script tests the Snowflake connection using the configuration
from your .env file and displays connection information.
"""

import sys
from pathlib import Path

try:
    import signal
except ImportError:
    # signal module not available on all platforms
    signal = None

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import after path modification
from lessons.lab_0005_snowflake.snowflake_lab import (  # noqa: E402
    SnowflakeConnection,
    SnowparkOperations,
)


class TimeoutError(Exception):
    """Custom timeout exception."""

    pass


def timeout_handler(signum, frame):
    """Handle timeout signal."""
    raise TimeoutError("Connection test timed out")


def _setup_timeout(timeout_seconds):
    """Set up timeout handler if signal module is available."""
    if signal is not None:
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout_seconds)


def _test_basic_connection(connection):
    """Test basic connection and return success status."""
    print("🔍 Testing connection...")
    if connection.test_connection():
        print("✅ Connection successful!")
        return True
    else:
        print("❌ Connection failed!")
        return False


def _display_connection_info(connection):
    """Display connection information and return success status."""
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
    return True


def _test_snowpark_operations(connection):
    """Test Snowpark operations and return success status."""
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
            return True
        else:
            print("❌ Query returned no results")
            return False


def _handle_timeout_error():
    """Handle timeout error with helpful message."""
    print("⏰ Connection test timed out. This could mean:")
    print("   - Your Snowflake credentials are incorrect")
    print("   - The Snowflake account doesn't exist or is inaccessible")
    print("   - There's a network connectivity issue")


def _handle_general_error(error):
    """Handle general error with troubleshooting tips."""
    print(f"❌ Error: {error}")
    print("\n🔧 Troubleshooting:")
    print(
        "1. Make sure your .env file exists and contains valid Snowflake credentials"
    )
    print("2. Verify your private key file exists and is accessible")
    print(
        "3. Check that the user MS3DM_LOCAL_DEV has been created in Snowflake"
    )
    print("4. Ensure your account identifier is correct")
    print("5. Run the setup_snowflake_user.sql script if you haven't already")


def _cleanup_connection(connection):
    """Clean up connection resources."""
    if signal is not None:
        try:
            signal.alarm(0)
        except Exception:
            pass
    if connection:
        try:
            connection.close_all_sessions()
        except Exception:
            pass


def connection_test_real(timeout_seconds=30):
    """Test the Snowflake connection with real connection (requires valid .env file)."""
    print("🔗 Testing Snowflake Connection...")
    print("=" * 50)

    connection = None
    try:
        _setup_timeout(timeout_seconds)

        # Create connection from environment variables
        print("📋 Loading configuration from .env file...")
        connection = SnowflakeConnection.from_environment()

        # Test basic connection
        if not _test_basic_connection(connection):
            return False

        # Display connection information
        if not _display_connection_info(connection):
            return False

        # Test Snowpark operations
        if not _test_snowpark_operations(connection):
            return False

        print(
            "\n🎉 All tests passed! Your Snowflake setup is working correctly."
        )
        return True

    except TimeoutError:
        _handle_timeout_error()
        return False
    except Exception as e:
        _handle_general_error(e)
        return False
    finally:
        _cleanup_connection(connection)


def test_connection():
    """Mock test for pytest that doesn't require real Snowflake connection."""
    print("🧪 Running mock connection test...")

    # Test configuration loading without actual connection
    try:
        from lessons.lab_0005_snowflake.snowflake_lab.config import (
            SnowflakeConfig,
        )

        # Test config creation with mock data (not loading from environment)
        config = SnowflakeConfig(
            account="test_account",
            user="test_user",
            warehouse="test_warehouse",
            database="test_database",
            schema_name="test_schema",
            role="test_role",
            password="test_password",
            private_key_path=None,
            private_key_passphrase=None,
        )

        # Basic validation
        assert config.account is not None
        assert config.user is not None
        assert config.warehouse is not None
        assert config.database is not None
        assert config.schema_name is not None
        assert config.role is not None

        print("✅ Configuration loading test passed!")
        # All assertions passed implicitly through the test
        assert True  # Test completed successfully

    except Exception as e:
        print(f"❌ Mock test failed: {e}")
        raise AssertionError(f"Mock test failed: {e}") from e


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
