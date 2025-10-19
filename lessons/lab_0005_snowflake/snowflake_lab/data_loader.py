"""Data loading utilities for ETL operations with Snowflake."""

import logging
from typing import Any

from snowflake.snowpark import DataFrame, Session
from snowflake.snowpark.exceptions import SnowparkSQLException

from .connection import SnowflakeConnection
from .dataframe_operations import SnowparkOperations


class DataLoader:
    """ETL utilities for loading data into Snowflake.

    This class provides methods for loading data from various sources
    into Snowflake tables, with support for different file formats
    and data transformation patterns.
    """

    def __init__(self, connection: SnowflakeConnection | Session):
        """Initialize the data loader.

        Args:
            connection: SnowflakeConnection or Snowpark Session
        """
        if isinstance(connection, SnowflakeConnection):
            self.connection = connection
            self.session = None
        else:
            self.connection = None
            self.session = connection

        self.ops = SnowparkOperations(connection)
        self._logger = logging.getLogger(__name__)

    def _get_session(self) -> Session:
        """Get the Snowpark session.

        Returns:
            Snowpark Session instance
        """
        if self.session is not None:
            return self.session
        elif self.connection is not None:
            return self.connection.get_session()
        else:
            raise ValueError("No session or connection available")

    def load_from_file(
        self,
        file_path: str,
        table_name: str,
        file_format: str = "csv",
        schema: str | None = None,
        mode: str = "append",
        **kwargs,
    ) -> None:
        """Load data from a file into a Snowflake table.

        Args:
            file_path: Path to the data file
            table_name: Target table name
            file_format: File format (csv, json, parquet, etc.)
            schema: Optional schema name
            mode: Write mode (append, overwrite, ignore)
            **kwargs: Additional file format options
        """
        session = self._get_session()

        if schema:
            full_table_name = f"{schema}.{table_name}"
        else:
            full_table_name = table_name

        try:
            # Read file based on format
            if file_format.lower() == "csv":
                df = self._read_csv_file(session, file_path, **kwargs)
            elif file_format.lower() == "json":
                df = self._read_json_file(session, file_path, **kwargs)
            elif file_format.lower() == "parquet":
                df = self._read_parquet_file(session, file_path, **kwargs)
            else:
                raise ValueError(f"Unsupported file format: {file_format}")

            # Write to table
            self.ops.write_to_table(df, table_name, mode, schema)
            self._logger.info(
                f"Successfully loaded {file_path} to {full_table_name}"
            )

        except Exception as e:
            self._logger.error(
                f"Failed to load {file_path} to {full_table_name}: {e}"
            )
            raise SnowparkSQLException(f"Failed to load data: {e}")

    def _read_csv_file(
        self, session: Session, file_path: str, **kwargs
    ) -> DataFrame:
        """Read CSV file into DataFrame.

        Args:
            session: Snowpark session
            file_path: Path to CSV file
            **kwargs: CSV options (delimiter, header, etc.)

        Returns:
            Snowpark DataFrame
        """
        # Default CSV options
        csv_options = {
            "field_delimiter": kwargs.get("delimiter", ","),
            "skip_header": kwargs.get("skip_header", 0),
            "field_optionally_enclosed_by": kwargs.get("quote_char", '"'),
            "null_if": kwargs.get("null_if", ""),
            "error_on_column_count_mismatch": kwargs.get(
                "error_on_column_count_mismatch", False
            ),
            "replace_invalid_characters": kwargs.get(
                "replace_invalid_characters", True
            ),
            "date_format": kwargs.get("date_format", "AUTO"),
            "timestamp_format": kwargs.get("timestamp_format", "AUTO"),
        }

        # Override with user-provided options
        csv_options.update(
            {
                k: v
                for k, v in kwargs.items()
                if k not in ["delimiter", "quote_char"]
            }
        )

        return session.read.options(**csv_options).csv(file_path)

    def _read_json_file(
        self, session: Session, file_path: str, **kwargs
    ) -> DataFrame:
        """Read JSON file into DataFrame.

        Args:
            session: Snowpark session
            file_path: Path to JSON file
            **kwargs: JSON options

        Returns:
            Snowpark DataFrame
        """
        # Default JSON options
        json_options = {
            "strip_outer_array": kwargs.get("strip_outer_array", False),
            "strip_null_values": kwargs.get("strip_null_values", False),
            "replace_invalid_characters": kwargs.get(
                "replace_invalid_characters", True
            ),
        }

        # Override with user-provided options
        json_options.update(
            {
                k: v
                for k, v in kwargs.items()
                if k not in ["strip_outer_array", "strip_null_values"]
            }
        )

        return session.read.options(**json_options).json(file_path)

    def _read_parquet_file(
        self, session: Session, file_path: str, **kwargs
    ) -> DataFrame:
        """Read Parquet file into DataFrame.

        Args:
            session: Snowpark session
            file_path: Path to Parquet file
            **kwargs: Parquet options

        Returns:
            Snowpark DataFrame
        """
        # Parquet files are read directly without special options
        return session.read.parquet(file_path)

    def load_from_dataframe(
        self,
        df: DataFrame,
        table_name: str,
        mode: str = "append",
        schema: str | None = None,
    ) -> None:
        """Load data from a DataFrame into a Snowflake table.

        Args:
            df: Source DataFrame
            table_name: Target table name
            mode: Write mode (append, overwrite, ignore)
            schema: Optional schema name
        """
        self.ops.write_to_table(df, table_name, mode, schema)
        self._logger.info(
            f"Successfully loaded DataFrame to {schema}.{table_name}"
            if schema
            else f"Successfully loaded DataFrame to {table_name}"
        )

    def load_from_query(
        self,
        query: str,
        table_name: str,
        mode: str = "append",
        schema: str | None = None,
    ) -> None:
        """Load data from a SQL query into a Snowflake table.

        Args:
            query: SQL query to execute
            table_name: Target table name
            mode: Write mode (append, overwrite, ignore)
            schema: Optional schema name
        """
        df = self.ops.read_sql(query)
        self.load_from_dataframe(df, table_name, mode, schema)

    def create_table_from_schema(
        self,
        table_name: str,
        schema_definition: list[dict[str, Any]],
        schema: str | None = None,
        if_not_exists: bool = True,
    ) -> None:
        """Create a table with a specific schema.

        Args:
            table_name: Name of the table to create
            schema_definition: List of column definitions
            schema: Optional schema name
            if_not_exists: Whether to use IF NOT EXISTS clause
        """
        session = self._get_session()

        if schema:
            full_table_name = f"{schema}.{table_name}"
        else:
            full_table_name = table_name

        # Build CREATE TABLE statement
        columns = []
        for col_def in schema_definition:
            col_name = col_def["name"]
            col_type = col_def["type"]
            nullable = "NULL" if col_def.get("nullable", True) else "NOT NULL"
            columns.append(f"{col_name} {col_type} {nullable}")

        if_not_exists_clause = "IF NOT EXISTS " if if_not_exists else ""
        create_sql = f"CREATE TABLE {if_not_exists_clause}{full_table_name} ({', '.join(columns)})"

        try:
            session.sql(create_sql).collect()
            self._logger.info(f"Successfully created table: {full_table_name}")
        except Exception as e:
            self._logger.error(
                f"Failed to create table {full_table_name}: {e}"
            )
            raise SnowparkSQLException(f"Failed to create table: {e}")

    def truncate_table(
        self, table_name: str, schema: str | None = None
    ) -> None:
        """Truncate a table (remove all data).

        Args:
            table_name: Name of the table to truncate
            schema: Optional schema name
        """
        session = self._get_session()

        if schema:
            full_table_name = f"{schema}.{table_name}"
        else:
            full_table_name = table_name

        try:
            session.sql(f"TRUNCATE TABLE {full_table_name}").collect()
            self._logger.info(
                f"Successfully truncated table: {full_table_name}"
            )
        except Exception as e:
            self._logger.error(
                f"Failed to truncate table {full_table_name}: {e}"
            )
            raise SnowparkSQLException(f"Failed to truncate table: {e}")

    def drop_table(
        self,
        table_name: str,
        schema: str | None = None,
        if_exists: bool = True,
    ) -> None:
        """Drop a table.

        Args:
            table_name: Name of the table to drop
            schema: Optional schema name
            if_exists: Whether to use IF EXISTS clause
        """
        session = self._get_session()

        if schema:
            full_table_name = f"{schema}.{table_name}"
        else:
            full_table_name = table_name

        if_exists_clause = "IF EXISTS " if if_exists else ""
        drop_sql = f"DROP TABLE {if_exists_clause}{full_table_name}"

        try:
            session.sql(drop_sql).collect()
            self._logger.info(f"Successfully dropped table: {full_table_name}")
        except Exception as e:
            self._logger.error(f"Failed to drop table {full_table_name}: {e}")
            raise SnowparkSQLException(f"Failed to drop table: {e}")

    def copy_data(
        self,
        source_table: str,
        target_table: str,
        source_schema: str | None = None,
        target_schema: str | None = None,
        where_clause: str | None = None,
    ) -> None:
        """Copy data from one table to another.

        Args:
            source_table: Source table name
            target_table: Target table name
            source_schema: Optional source schema name
            target_schema: Optional target schema name
            where_clause: Optional WHERE clause for filtering
        """
        session = self._get_session()

        # Build table names
        if source_schema:
            full_source_table = f"{source_schema}.{source_table}"
        else:
            full_source_table = source_table

        if target_schema:
            full_target_table = f"{target_schema}.{target_table}"
        else:
            full_target_table = target_table

        # Build COPY statement
        where_clause_sql = f" WHERE {where_clause}" if where_clause else ""
        copy_sql = f"INSERT INTO {full_target_table} SELECT * FROM {full_source_table}{where_clause_sql}"

        try:
            session.sql(copy_sql).collect()
            self._logger.info(
                f"Successfully copied data from {full_source_table} to {full_target_table}"
            )
        except Exception as e:
            self._logger.error(f"Failed to copy data: {e}")
            raise SnowparkSQLException(f"Failed to copy data: {e}")

    def get_table_info(
        self, table_name: str, schema: str | None = None
    ) -> dict[str, Any]:
        """Get information about a table.

        Args:
            table_name: Name of the table
            schema: Optional schema name

        Returns:
            Dictionary with table information
        """
        session = self._get_session()

        if schema:
            full_table_name = f"{schema}.{table_name}"
        else:
            full_table_name = table_name

        try:
            # Get table description
            desc_result = session.sql(
                f"DESCRIBE TABLE {full_table_name}"
            ).collect()
            columns = [row.asDict() for row in desc_result]

            # Get row count
            count_result = session.sql(
                f"SELECT COUNT(*) as row_count FROM {full_table_name}"
            ).collect()
            row_count = count_result[0]["ROW_COUNT"] if count_result else 0

            return {
                "table_name": full_table_name,
                "columns": columns,
                "row_count": row_count,
            }
        except Exception as e:
            self._logger.error(
                f"Failed to get table info for {full_table_name}: {e}"
            )
            raise SnowparkSQLException(f"Failed to get table info: {e}")

    def __repr__(self) -> str:
        """String representation of the data loader."""
        return f"DataLoader(connection={self.connection is not None}, session={self.session is not None})"
