"""
Configuration-driven Snowflake environment setup.

This module provides utilities for setting up Snowflake environments
using configuration files and the lab_0002 config loader.
"""

import logging
from pathlib import Path
from typing import Any

from snowflake.snowpark import Session  # type: ignore
from snowflake.snowpark.exceptions import SnowparkSQLException  # type: ignore

from lessons.lab_0002_config_loader.config_loader import ConfigManager

from .config import SnowflakeConfig
from .connection import SnowflakeConnection
from .database_manager import DatabaseManager
from .environment_config import (
    DatabaseConfig,
    RoleConfig,
    SchemaConfig,
    TableConfig,
    UserConfig,
    WarehouseConfig,
)

logger = logging.getLogger(__name__)


class SnowflakeConfigSetup:
    """
    Handles configuration-driven setup of Snowflake environments.
    """

    def __init__(self, config_file: str):
        """
        Initialize the config setup.

        Args:
            config_file: Path to the configuration file (JSON, YAML, TOML, or
            .env)
        """
        self.config_file = Path(config_file)
        self.config_manager = ConfigManager.load_from_file(
            str(self.config_file)
        )
        self.connection: SnowflakeConnection | None = None
        self.session: Session | None = None
        self.db_manager: DatabaseManager | None = None

    def connect(self) -> bool:
        """
        Establish connection to Snowflake using the configuration.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Load environment variables from .env file first
            from dotenv import load_dotenv

            load_dotenv()

            # Get connection parameters from config
            connection_config = self.config_manager.get("connection", {})

            # Resolve environment variables in the config
            import os

            resolved_config = {}
            for key, value in connection_config.items():
                if (
                    isinstance(value, str)
                    and value.startswith("${")
                    and value.endswith("}")
                ):
                    env_var = value[2:-1]  # Remove ${ and }
                    resolved_value = os.getenv(env_var, value)
                    resolved_config[key] = resolved_value
                else:
                    resolved_config[key] = value

            # Set environment variables for the connection manager
            for key, value in resolved_config.items():
                if value is not None:
                    os.environ[f"SNOWFLAKE_{key.upper()}"] = str(value)

            # Create SnowflakeConnection instance using resolved config
            logger.debug(
                f"Creating SnowflakeConfig with resolved config: {resolved_config}"
            )
            config = SnowflakeConfig(**resolved_config)
            self.connection = SnowflakeConnection(config)

            # Create session
            if self.connection:
                self.session = self.connection.get_session()
                self.db_manager = DatabaseManager(self.session)
            else:
                raise RuntimeError("Failed to create SnowflakeConnection")

            logger.info("Successfully connected to Snowflake")
            return True

        except Exception as e:
            logger.error(f"Failed to connect to Snowflake: {e}")
            return False

    def setup_database(self, db_config: DatabaseConfig) -> bool:
        """
        Set up a database based on configuration.

        Args:
            db_config: Database configuration

        Returns:
            True if successful, False otherwise
        """
        if not self.db_manager:
            logger.error(
                "Database manager not initialized. Call connect() first."
            )
            return False

        return self.db_manager.create_database(
            database_name=db_config.name,
            if_not_exists=db_config.if_not_exists,
            comment=db_config.comment,
            data_retention_time_in_days=db_config.data_retention_time_in_days,
        )

    def setup_schema(self, schema_config: SchemaConfig) -> bool:
        """
        Set up a schema based on configuration.

        Args:
            schema_config: Schema configuration

        Returns:
            True if successful, False otherwise
        """
        if not self.db_manager:
            logger.error(
                "Database manager not initialized. Call connect() first."
            )
            return False

        return self.db_manager.create_schema(
            schema_name=schema_config.schema_name,
            database_name=schema_config.database,
            if_not_exists=schema_config.if_not_exists,
            comment=schema_config.comment,
            managed_access=schema_config.managed_access,
        )

    def setup_warehouse(self, warehouse_config: WarehouseConfig) -> bool:
        """
        Set up a warehouse based on configuration.

        Args:
            warehouse_config: Warehouse configuration

        Returns:
            True if successful, False otherwise
        """
        if not self.db_manager:
            logger.error(
                "Database manager not initialized. Call connect() first."
            )
            return False

        return self.db_manager.create_warehouse(
            warehouse_name=warehouse_config.name,
            if_not_exists=warehouse_config.if_not_exists,
            warehouse_size=warehouse_config.size,
            auto_suspend=warehouse_config.auto_suspend,
            auto_resume=warehouse_config.auto_resume,
            comment=warehouse_config.comment,
        )

    def setup_roles(self, roles: list[RoleConfig]) -> dict[str, bool]:
        """
        Set up roles based on configuration.

        Args:
            roles: List of role configurations

        Returns:
            Dictionary with setup results for each role
        """
        if not self.session:
            logger.error("Session not initialized. Call connect() first.")
            return {}

        results = {}
        for role_config in roles:
            try:
                if_not_exists_clause = (
                    "IF NOT EXISTS " if role_config.if_not_exists else ""
                )
                comment_clause = (
                    f" COMMENT = '{role_config.comment}'"
                    if role_config.comment
                    else ""
                )

                sql = f"CREATE ROLE {if_not_exists_clause}{role_config.name}{comment_clause};"
                logger.info(f"Creating role: {role_config.name}")

                self.session.sql(sql).collect()
                results[role_config.name] = True
                logger.info(f"Role '{role_config.name}' created successfully")

            except SnowparkSQLException as e:
                logger.error(
                    f"Failed to create role '{role_config.name}': {e}"
                )
                results[role_config.name] = False

        return results

    def setup_users(self, users: list[UserConfig]) -> dict[str, bool]:
        """
        Set up users based on configuration.

        Args:
            users: List of user configurations

        Returns:
            Dictionary with setup results for each user
        """
        if not self.session:
            logger.error("Session not initialized. Call connect() first.")
            return {}

        results = {}
        for user_config in users:
            try:
                if_not_exists_clause = (
                    "IF NOT EXISTS " if user_config.if_not_exists else ""
                )
                display_name_clause = (
                    f" DISPLAY_NAME = '{user_config.display_name}'"
                    if user_config.display_name
                    else ""
                )
                email_clause = (
                    f" EMAIL = '{user_config.email}'"
                    if user_config.email
                    else ""
                )
                default_role_clause = (
                    f" DEFAULT_ROLE = {user_config.default_role}"
                    if user_config.default_role
                    else ""
                )
                default_warehouse_clause = (
                    f" DEFAULT_WAREHOUSE = {user_config.default_warehouse}"
                    if user_config.default_warehouse
                    else ""
                )
                default_namespace_clause = (
                    f" DEFAULT_NAMESPACE = {user_config.default_namespace}"
                    if user_config.default_namespace
                    else ""
                )
                rsa_key_clause = (
                    f" RSA_PUBLIC_KEY = '{user_config.rsa_public_key}'"
                    if user_config.rsa_public_key
                    else ""
                )
                comment_clause = (
                    f" COMMENT = '{user_config.comment}'"
                    if user_config.comment
                    else ""
                )
                must_change_clause = f" MUST_CHANGE_PASSWORD = {str(user_config.must_change_password).upper()}"

                sql = (
                    f"CREATE USER {if_not_exists_clause}{user_config.name}"
                    f"{display_name_clause}{email_clause}{default_role_clause}"
                    f"{default_warehouse_clause}{default_namespace_clause}"
                    f"{rsa_key_clause}{comment_clause}{must_change_clause};"
                )

                logger.info(f"Creating user: {user_config.name}")
                self.session.sql(sql).collect()
                results[user_config.name] = True
                logger.info(f"User '{user_config.name}' created successfully")

            except SnowparkSQLException as e:
                logger.error(
                    f"Failed to create user '{user_config.name}': {e}"
                )
                results[user_config.name] = False

        return results

    def setup_tables(self, tables: list[TableConfig]) -> dict[str, bool]:
        """
        Set up tables based on configuration.

        Args:
            tables: List of table configurations

        Returns:
            Dictionary with setup results for each table
        """
        if not self.session:
            logger.error("Session not initialized. Call connect() first.")
            return {}

        results = {}
        for table_config in tables:
            try:
                # Build full table name
                db_name = table_config.database or self.config_manager.get(
                    "connection.database"
                )
                schema_name = (
                    table_config.schema_name
                    or self.config_manager.get("connection.schema_name")
                )
                full_table_name = (
                    f"{db_name}.{schema_name}.{table_config.name}"
                )

                if_not_exists_clause = (
                    "IF NOT EXISTS " if table_config.if_not_exists else ""
                )
                comment_clause = (
                    f" COMMENT = '{table_config.comment}'"
                    if table_config.comment
                    else ""
                )

                # Build column definitions
                columns_sql = ", ".join(
                    [
                        f"{col['name']} {col['type']}"
                        + ("" if col.get("nullable", True) else " NOT NULL")
                        + (
                            f" COMMENT '{col['comment']}'"
                            if col.get("comment")
                            else ""
                        )
                        for col in table_config.columns
                    ]
                )

                sql = f"CREATE TABLE {if_not_exists_clause}{full_table_name} ({columns_sql}){comment_clause};"

                logger.info(f"Creating table: {full_table_name}")
                self.session.sql(sql).collect()
                results[table_config.name] = True
                logger.info(f"Table '{full_table_name}' created successfully")

            except SnowparkSQLException as e:
                logger.error(
                    f"Failed to create table '{table_config.name}': {e}"
                )
                results[table_config.name] = False

        return results

    def execute_grants(self, grants: list[dict[str, Any]]) -> dict[str, bool]:
        """
        Execute grant statements based on configuration.

        Args:
            grants: List of grant configurations

        Returns:
            Dictionary with execution results for each grant
        """
        if not self.session:
            logger.error("Session not initialized. Call connect() first.")
            return {}

        results = {}
        for i, grant in enumerate(grants):
            try:
                sql = grant.get("sql", "")
                if not sql:
                    logger.warning(f"Grant {i} has no SQL statement, skipping")
                    continue

                logger.info(f"Executing grant: {sql}")
                self.session.sql(sql).collect()
                results[f"grant_{i}"] = True
                logger.info(f"Grant {i} executed successfully")

            except SnowparkSQLException as e:
                logger.error(f"Failed to execute grant {i}: {e}")
                results[f"grant_{i}"] = False

        return results

    def setup_environment(self) -> dict[str, Any]:
        """
        Set up the complete Snowflake environment based on configuration.

        Returns:
            Dictionary with setup results for all components
        """
        if not self.connect():
            return {"error": "Failed to connect to Snowflake"}

        results: dict[str, Any] = {"connection": True}

        # Get environment configuration
        env_config = self.config_manager.get("environment", {})
        if not env_config:
            logger.warning("No environment configuration found")
            return results

        # Set up database
        if "database" in env_config:
            db_config = DatabaseConfig(**env_config["database"])
            results["database"] = self.setup_database(db_config)

        # Set up schema
        if "schema" in env_config:
            schema_config = SchemaConfig(**env_config["schema"])
            results["schema"] = self.setup_schema(schema_config)

        # Set up warehouse
        if "warehouse" in env_config:
            warehouse_config = WarehouseConfig(**env_config["warehouse"])
            results["warehouse"] = self.setup_warehouse(warehouse_config)

        # Set up roles
        if "roles" in env_config:
            roles = [RoleConfig(**role) for role in env_config["roles"]]
            role_results = self.setup_roles(roles)
            results["roles"] = role_results

        # Set up users
        if "users" in env_config:
            users = [UserConfig(**user) for user in env_config["users"]]
            user_results = self.setup_users(users)
            results["users"] = user_results

        # Set up tables
        if "tables" in env_config:
            tables = [TableConfig(**table) for table in env_config["tables"]]
            table_results = self.setup_tables(tables)
            results["tables"] = table_results

        # Execute grants
        if "grants" in env_config:
            grant_results = self.execute_grants(env_config["grants"])
            results["grants"] = grant_results

        return results

    def close(self):
        """Close the Snowflake session."""
        if self.connection:
            self.connection.close_all_sessions()
            self.connection = None
            self.session = None
            self.db_manager = None
