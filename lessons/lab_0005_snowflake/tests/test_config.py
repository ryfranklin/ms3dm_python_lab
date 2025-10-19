"""Tests for the Snowflake configuration module."""

import tempfile
from pathlib import Path

import pytest

from lessons.lab_0005_snowflake.snowflake_lab.config import SnowflakeConfig


class TestSnowflakeConfig:
    """Test cases for SnowflakeConfig."""

    def test_init_with_key_pair_auth(self):
        """Test initialization with key pair authentication."""
        with tempfile.NamedTemporaryFile(suffix=".pem", delete=False) as f:
            f.write(
                b"-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCzJSj+1yrMUz3y\n-----END PRIVATE KEY-----"
            )
            f.flush()

            config = SnowflakeConfig(
                account="test_account",
                user="test_user",
                warehouse="test_warehouse",
                database="test_database",
                schema_name="test_schema",
                role="test_role",
                private_key_path=f.name,
            )

            assert config.account == "test_account"
            assert config.user == "test_user"
            assert config.private_key_path == f.name
            assert config.password is None

            # Clean up
            Path(f.name).unlink()

    def test_init_with_password_auth(self):
        """Test initialization with password authentication."""
        config = SnowflakeConfig(
            account="test_account",
            user="test_user",
            warehouse="test_warehouse",
            database="test_database",
            schema_name="test_schema",
            role="test_role",
            password="test_password",
        )

        assert config.account == "test_account"
        assert config.user == "test_user"
        assert config.password == "test_password"
        assert config.private_key_path is None

    def test_init_with_defaults(self):
        """Test initialization with default values."""
        config = SnowflakeConfig(
            account="test_account",
            user="test_user",
            warehouse="test_warehouse",
            database="test_database",
            schema_name="test_schema",
            role="test_role",
        )

        assert config.connection_timeout == 60
        assert config.query_timeout == 300
        assert config.max_connections == 10
        assert config.application_name == "snowflake-lab"
        assert config.log_level == "INFO"

    def test_validate_auth_method_key_pair(self):
        """Test authentication method validation with key pair."""
        with tempfile.NamedTemporaryFile(suffix=".pem", delete=False) as f:
            f.write(
                b"-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCzJSj+1yrMUz3y\n-----END PRIVATE KEY-----"
            )
            f.flush()

            config = SnowflakeConfig(
                account="test_account",
                user="test_user",
                warehouse="test_warehouse",
                database="test_database",
                schema_name="test_schema",
                role="test_role",
                private_key_path=f.name,
            )

            auth_method = config.validate_auth_method()
            assert auth_method == "key_pair"

            # Clean up
            Path(f.name).unlink()

    def test_validate_auth_method_password(self):
        """Test authentication method validation with password."""
        config = SnowflakeConfig(
            account="test_account",
            user="test_user",
            warehouse="test_warehouse",
            database="test_database",
            schema_name="test_schema",
            role="test_role",
            password="test_password",
        )

        auth_method = config.validate_auth_method()
        assert auth_method == "password"

    def test_validate_auth_method_both_provided(self):
        """Test validation error when both auth methods provided."""
        with tempfile.NamedTemporaryFile(suffix=".pem", delete=False) as f:
            f.write(
                b"-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCzJSj+1yrMUz3y\n-----END PRIVATE KEY-----"
            )
            f.flush()

            config = SnowflakeConfig(
                account="test_account",
                user="test_user",
                warehouse="test_warehouse",
                database="test_database",
                schema_name="test_schema",
                role="test_role",
                private_key_path=f.name,
                password="test_password",
            )

            with pytest.raises(
                ValueError,
                match="Cannot specify both key pair and password authentication",
            ):
                config.validate_auth_method()

            # Clean up
            Path(f.name).unlink()

    def test_validate_auth_method_none_provided(self):
        """Test validation error when no auth method provided."""
        config = SnowflakeConfig(
            account="test_account",
            user="test_user",
            warehouse="test_warehouse",
            database="test_database",
            schema_name="test_schema",
            role="test_role",
        )

        with pytest.raises(
            ValueError,
            match="Must specify either private_key_path or password",
        ):
            config.validate_auth_method()

    def test_validate_log_level_valid(self):
        """Test log level validation with valid values."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

        for level in valid_levels:
            config = SnowflakeConfig(
                account="test_account",
                user="test_user",
                warehouse="test_warehouse",
                database="test_database",
                schema_name="test_schema",
                role="test_role",
                password="test_password",
                log_level=level,
            )
            assert config.log_level == level.upper()

    def test_validate_log_level_invalid(self):
        """Test log level validation with invalid value."""
        with pytest.raises(ValueError, match="Invalid log level"):
            SnowflakeConfig(
                account="test_account",
                user="test_user",
                warehouse="test_warehouse",
                database="test_database",
                schema_name="test_schema",
                role="test_role",
                password="test_password",
                log_level="INVALID",
            )

    def test_validate_private_key_path_nonexistent(self):
        """Test private key path validation with nonexistent file."""
        with pytest.raises(ValueError, match="Private key file not found"):
            SnowflakeConfig(
                account="test_account",
                user="test_user",
                warehouse="test_warehouse",
                database="test_database",
                schema_name="test_schema",
                role="test_role",
                private_key_path="/nonexistent/key.pem",
            )

    def test_validate_private_key_path_directory(self):
        """Test private key path validation with directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with pytest.raises(
                ValueError, match="Private key path is not a file"
            ):
                SnowflakeConfig(
                    account="test_account",
                    user="test_user",
                    warehouse="test_warehouse",
                    database="test_database",
                    schema_name="test_schema",
                    role="test_role",
                    private_key_path=temp_dir,
                )

    def test_get_connection_parameters_key_pair(self):
        """Test getting connection parameters with key pair auth."""
        # Create a valid RSA private key for testing
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import rsa

        # Generate a test private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        # Serialize to PEM format
        pem_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        with tempfile.NamedTemporaryFile(suffix=".pem", delete=False) as f:
            f.write(pem_private_key)
            f.flush()

            config = SnowflakeConfig(
                account="test_account",
                user="test_user",
                warehouse="test_warehouse",
                database="test_database",
                schema_name="test_schema",
                role="test_role",
                private_key_path=f.name,
            )

            params = config.get_connection_parameters()

            assert params["account"] == "test_account"
            assert params["user"] == "test_user"
            assert params["warehouse"] == "test_warehouse"
            assert params["database"] == "test_database"
            assert params["schema"] == "test_schema"
            assert params["role"] == "test_role"
            assert "private_key" in params
            assert "password" not in params

            # Clean up
            Path(f.name).unlink()

    def test_get_connection_parameters_password(self):
        """Test getting connection parameters with password auth."""
        config = SnowflakeConfig(
            account="test_account",
            user="test_user",
            warehouse="test_warehouse",
            database="test_database",
            schema_name="test_schema",
            role="test_role",
            password="test_password",
        )

        params = config.get_connection_parameters()

        assert params["account"] == "test_account"
        assert params["user"] == "test_user"
        assert params["password"] == "test_password"
        assert "private_key" not in params

    def test_from_config_file(self):
        """Test loading configuration from file."""
        config_data = {
            "account": "test_account",
            "user": "test_user",
            "warehouse": "test_warehouse",
            "database": "test_database",
            "schema_name": "test_schema",
            "role": "test_role",
            "password": "test_password",
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            import json

            json.dump(config_data, f)
            f.flush()

            config = SnowflakeConfig.from_config_file(f.name)

            assert config.account == "test_account"
            assert config.user == "test_user"
            assert config.password == "test_password"

            # Clean up
            Path(f.name).unlink()

    def test_from_env_file(self):
        """Test loading configuration from .env file."""
        env_content = """SNOWFLAKE_ACCOUNT=test_account
SNOWFLAKE_USER=test_user
SNOWFLAKE_WAREHOUSE=test_warehouse
SNOWFLAKE_DATABASE=test_database
SNOWFLAKE_SCHEMA=test_schema
SNOWFLAKE_ROLE=test_role
SNOWFLAKE_PASSWORD=test_password
SNOWFLAKE_CONNECTION_TIMEOUT=120
SNOWFLAKE_LOG_LEVEL=DEBUG
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".env", delete=False
        ) as f:
            f.write(env_content)
            f.flush()

            # Temporarily clear environment variables to avoid interference
            import os

            original_env = {}
            env_vars_to_clear = [
                "SNOWFLAKE_ACCOUNT",
                "SNOWFLAKE_USER",
                "SNOWFLAKE_WAREHOUSE",
                "SNOWFLAKE_DATABASE",
                "SNOWFLAKE_SCHEMA",
                "SNOWFLAKE_ROLE",
                "SNOWFLAKE_PASSWORD",
                "SNOWFLAKE_CONNECTION_TIMEOUT",
                "SNOWFLAKE_LOG_LEVEL",
            ]

            for var in env_vars_to_clear:
                if var in os.environ:
                    original_env[var] = os.environ[var]
                    del os.environ[var]

            try:
                config = SnowflakeConfig.from_env_file(f.name)

                assert config.account == "test_account"
                assert config.user == "test_user"
                assert config.password == "test_password"
                assert config.connection_timeout == 120
                assert config.log_level == "DEBUG"
            finally:
                # Restore original environment
                for var, value in original_env.items():
                    os.environ[var] = value

            # Clean up
            Path(f.name).unlink()

    def test_to_dict(self):
        """Test converting configuration to dictionary."""
        config = SnowflakeConfig(
            account="test_account",
            user="test_user",
            warehouse="test_warehouse",
            database="test_database",
            schema_name="test_schema",
            role="test_role",
            password="test_password",
        )

        config_dict = config.to_dict()

        assert config_dict["account"] == "test_account"
        assert config_dict["user"] == "test_user"
        assert config_dict["password"] == "test_password"
        assert config_dict["private_key_path"] is None

    def test_repr(self):
        """Test string representation."""
        config = SnowflakeConfig(
            account="test_account",
            user="test_user",
            warehouse="test_warehouse",
            database="test_database",
            schema_name="test_schema",
            role="test_role",
            password="test_password",
        )

        repr_str = repr(config)
        assert "SnowflakeConfig" in repr_str
        assert "test_account" in repr_str
        assert "test_user" in repr_str
        assert "password" in repr_str
