"""
Database and Schema Management for Snowflake Lab.

This module provides utilities for creating and managing databases, schemas,
and other Snowflake objects using configuration-driven approaches.
"""

import logging
from typing import Any

from snowflake.snowpark import Session  # type: ignore
from snowflake.snowpark.exceptions import SnowparkSQLException  # type: ignore

from .config import SnowflakeConfig

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Manages Snowflake databases, schemas, and related objects
    using configuration-driven approaches.
    """

    def __init__(
        self, session: Session, config: SnowflakeConfig | None = None
    ):
        """
        Initialize the database manager.

        Args:
            session: Active Snowpark session
            config: Snowflake configuration (optional, will load from environment if not provided)
        """
        self.session = session
        self.config = config or SnowflakeConfig(  # type: ignore
            account="default_account",
            user="default_user",
            warehouse="default_warehouse",
            database="default_database",
            schema_name="default_schema",
            role="default_role",
        )
        logger.info("DatabaseManager initialized")

    def create_database(
        self,
        database_name: str,
        if_not_exists: bool = True,
        comment: str | None = None,
        data_retention_time_in_days: int | None = None,
    ) -> bool:
        """
        Create a Snowflake database.

        Args:
            database_name: Name of the database to create
            if_not_exists: If True, adds IF NOT EXISTS clause
            comment: Optional comment for the database
            data_retention_time_in_days: Data retention period in days

        Returns:
            True if successful, False otherwise
        """
        try:
            if_not_exists_clause = "IF NOT EXISTS " if if_not_exists else ""
            comment_clause = f" COMMENT = '{comment}'" if comment else ""
            retention_clause = (
                f" DATA_RETENTION_TIME_IN_DAYS = {data_retention_time_in_days}"
                if data_retention_time_in_days
                else ""
            )

            sql = f"CREATE DATABASE {if_not_exists_clause}{database_name}{comment_clause}{retention_clause};"
            logger.info(f"Creating database: {database_name}")

            self.session.sql(sql).collect()
            logger.info(f"Database '{database_name}' created successfully")
            return True

        except SnowparkSQLException as e:
            logger.error(f"Failed to create database '{database_name}': {e}")
            return False

    def create_schema(
        self,
        schema_name: str,
        database_name: str | None = None,
        if_not_exists: bool = True,
        comment: str | None = None,
        managed_access: bool = False,
    ) -> bool:
        """
        Create a Snowflake schema.

        Args:
            schema_name: Name of the schema to create
            database_name: Database name (uses config default if not provided)
            if_not_exists: If True, adds IF NOT EXISTS clause
            comment: Optional comment for the schema
            managed_access: If True, enables managed access

        Returns:
            True if successful, False otherwise
        """
        try:
            db_name = database_name or self.config.database
            if_not_exists_clause = "IF NOT EXISTS " if if_not_exists else ""
            comment_clause = f" COMMENT = '{comment}'" if comment else ""
            managed_clause = " WITH MANAGED ACCESS" if managed_access else ""

            sql = f"CREATE SCHEMA {if_not_exists_clause}{db_name}.{schema_name}{managed_clause}{comment_clause};"
            logger.info(f"Creating schema: {db_name}.{schema_name}")

            self.session.sql(sql).collect()
            logger.info(
                f"Schema '{db_name}.{schema_name}' created successfully"
            )
            return True

        except SnowparkSQLException as e:
            logger.error(f"Failed to create schema '{schema_name}': {e}")
            return False

    def create_warehouse(
        self,
        warehouse_name: str,
        if_not_exists: bool = True,
        warehouse_size: str = "X-SMALL",
        auto_suspend: int = 60,
        auto_resume: bool = True,
        comment: str | None = None,
    ) -> bool:
        """
        Create a Snowflake warehouse.

        Args:
            warehouse_name: Name of the warehouse to create
            if_not_exists: If True, adds IF NOT EXISTS clause
            warehouse_size: Size of the warehouse (X-SMALL, SMALL, MEDIUM, LARGE, etc.)
            auto_suspend: Auto-suspend time in seconds
            auto_resume: Whether to auto-resume the warehouse
            comment: Optional comment for the warehouse

        Returns:
            True if successful, False otherwise
        """
        try:
            if_not_exists_clause = "IF NOT EXISTS " if if_not_exists else ""
            comment_clause = f" COMMENT = '{comment}'" if comment else ""
            auto_resume_clause = (
                " AUTO_RESUME = TRUE"
                if auto_resume
                else " AUTO_RESUME = FALSE"
            )

            sql = (
                f"CREATE WAREHOUSE {if_not_exists_clause}{warehouse_name} "
                f"WAREHOUSE_SIZE = {warehouse_size} "
                f"AUTO_SUSPEND = {auto_suspend}{auto_resume_clause}{comment_clause};"
            )
            logger.info(f"Creating warehouse: {warehouse_name}")

            self.session.sql(sql).collect()
            logger.info(f"Warehouse '{warehouse_name}' created successfully")
            return True

        except SnowparkSQLException as e:
            logger.error(f"Failed to create warehouse '{warehouse_name}': {e}")
            return False

    def setup_environment_from_config(
        self, config_file: str | None = None
    ) -> dict[str, bool]:
        """
        Set up the complete Snowflake environment based on configuration.

        Args:
            config_file: Optional path to configuration file

        Returns:
            Dictionary with setup results for each component
        """
        if config_file:
            # Reload config from file
            from lessons.lab_0002_config_loader.config_loader import (
                ConfigManager,
            )

            ConfigManager.load_from_file(config_file)
            # This would need to be adapted based on your config structure
            logger.info(f"Loading configuration from: {config_file}")

        results = {}

        # Note: This method expects a more complex config structure
        # For now, we'll just return a basic result since the current
        # SnowflakeConfig doesn't have environment attributes
        logger.warning(
            "Environment setup requires a more complex config structure"
        )
        results["status"] = "skipped - requires environment config"

        return results

    def get_database_info(self, database_name: str) -> dict[str, Any] | None:
        """
        Get information about a database.

        Args:
            database_name: Name of the database

        Returns:
            Dictionary with database information or None if not found
        """
        try:
            result = self.session.sql(
                f"SHOW DATABASES LIKE '{database_name}'"
            ).collect()
            if result:
                return dict(result[0])
            return None
        except SnowparkSQLException as e:
            logger.error(
                f"Failed to get database info for '{database_name}': {e}"
            )
            return None

    def get_schema_info(
        self, schema_name: str, database_name: str | None = None
    ) -> dict[str, Any] | None:
        """
        Get information about a schema.

        Args:
            schema_name: Name of the schema
            database_name: Database name (uses config default if not provided)

        Returns:
            Dictionary with schema information or None if not found
        """
        try:
            db_name = database_name or self.config.database
            result = self.session.sql(
                f"SHOW SCHEMAS IN DATABASE {db_name} LIKE '{schema_name}'"
            ).collect()
            if result:
                return dict(result[0])
            return None
        except SnowparkSQLException as e:
            logger.error(f"Failed to get schema info for '{schema_name}': {e}")
            return None

    def list_databases(self) -> list[dict[str, Any]]:
        """
        List all databases accessible to the current user.

        Returns:
            List of dictionaries with database information
        """
        try:
            result = self.session.sql("SHOW DATABASES").collect()
            return [dict(row) for row in result]
        except SnowparkSQLException as e:
            logger.error(f"Failed to list databases: {e}")
            return []

    def list_schemas(
        self, database_name: str | None = None
    ) -> list[dict[str, Any]]:
        """
        List all schemas in a database.

        Args:
            database_name: Database name (uses config default if not provided)

        Returns:
            List of dictionaries with schema information
        """
        db_name = database_name or self.config.database
        try:
            result = self.session.sql(
                f"SHOW SCHEMAS IN DATABASE {db_name}"
            ).collect()
            return [dict(row) for row in result]
        except SnowparkSQLException as e:
            logger.error(
                f"Failed to list schemas in database '{db_name}': {e}"
            )
            return []
