"""Snowflake Lab - A comprehensive Snowpark integration for Python data engineering.

This module provides a complete toolkit for working with Snowflake using Snowpark,
including connection management, DataFrame operations, data loading, and ETL patterns.

Key Features:
- Key-pair and password authentication
- Connection management with pooling
- Snowpark DataFrame operations
- Data loading and ETL utilities
- Query builders and optimization
- Integration with lab_0002 config loader

Example:
    from snowflake_lab import SnowflakeConnection, SnowparkOperations

    # Connect to Snowflake
    conn = SnowflakeConnection.from_config("snowflake_config.yaml")

    # Create Snowpark session
    session = conn.get_session()

    # Work with DataFrames
    ops = SnowparkOperations(session)
    df = ops.read_table("my_table")
    result = df.filter(df.col("amount") > 100).collect()
"""

from .config import SnowflakeConfig
from .config_setup import SnowflakeConfigSetup
from .connection import SnowflakeConnection
from .data_loader import DataLoader
from .database_manager import DatabaseManager
from .dataframe_operations import SnowparkOperations
from .environment_config import (
    DatabaseConfig,
    EnvironmentConfig,
    RoleConfig,
    SchemaConfig,
    SnowflakeEnvironmentConfig,
    TableConfig,
    UserConfig,
    WarehouseConfig,
)
from .query_builder import QueryBuilder

__all__ = [
    "SnowflakeConfig",
    "SnowflakeConnection",
    "SnowparkOperations",
    "DataLoader",
    "QueryBuilder",
    "DatabaseManager",
    "DatabaseConfig",
    "SchemaConfig",
    "WarehouseConfig",
    "RoleConfig",
    "UserConfig",
    "TableConfig",
    "EnvironmentConfig",
    "SnowflakeEnvironmentConfig",
    "SnowflakeConfigSetup",
]

__version__ = "1.0.0"
