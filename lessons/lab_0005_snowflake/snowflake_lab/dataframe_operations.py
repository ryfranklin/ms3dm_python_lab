"""Snowpark DataFrame operations and transformations."""

import logging
from typing import Any

from snowflake.snowpark import DataFrame, Session
from snowflake.snowpark.exceptions import SnowparkSQLException
from snowflake.snowpark.functions import avg, col, count
from snowflake.snowpark.functions import max as sf_max
from snowflake.snowpark.functions import min as sf_min
from snowflake.snowpark.functions import sum as sf_sum

from .connection import SnowflakeConnection


class SnowparkOperations:
    """High-level operations for working with Snowpark DataFrames.

    This class provides convenient methods for common DataFrame operations,
    data transformations, and analytics queries using Snowpark.
    """

    def __init__(self, connection: SnowflakeConnection | Session):
        """Initialize the operations handler.

        Args:
            connection: SnowflakeConnection or Snowpark Session
        """
        if isinstance(connection, SnowflakeConnection):
            self.connection = connection
            self.session = None
        else:
            self.connection = None
            self.session = connection

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

    def read_table(
        self, table_name: str, schema: str | None = None
    ) -> DataFrame:
        """Read data from a Snowflake table.

        Args:
            table_name: Name of the table
            schema: Optional schema name (uses current schema if not provided)

        Returns:
            Snowpark DataFrame
        """
        session = self._get_session()

        if schema:
            full_table_name = f"{schema}.{table_name}"
        else:
            full_table_name = table_name

        try:
            df = session.table(full_table_name)
            self._logger.info(f"Successfully read table: {full_table_name}")
            return df
        except Exception as e:
            self._logger.error(f"Failed to read table {full_table_name}: {e}")
            raise SnowparkSQLException(f"Failed to read table: {e}") from e

    def read_sql(self, sql: str) -> DataFrame:
        """Read data using a SQL query.

        Args:
            sql: SQL query string

        Returns:
            Snowpark DataFrame
        """
        session = self._get_session()

        try:
            df = session.sql(sql)
            self._logger.info("Successfully executed SQL query")
            return df
        except Exception as e:
            self._logger.error(f"Failed to execute SQL query: {e}")
            raise SnowparkSQLException(f"SQL query failed: {e}") from e

    def filter_data(
        self, df: DataFrame, conditions: dict[str, Any]
    ) -> DataFrame:
        """Filter DataFrame based on conditions.

        Args:
            df: Input DataFrame
            conditions: Dictionary of column conditions {column: value}

        Returns:
            Filtered DataFrame
        """
        filtered_df = df

        for column, value in conditions.items():
            if isinstance(value, tuple) and len(value) == 2:
                # Range condition (min, max)
                min_val, max_val = value
                filtered_df = filtered_df.filter(
                    (col(column) >= min_val) & (col(column) <= max_val)
                )
            elif isinstance(value, list):
                # IN condition
                filtered_df = filtered_df.filter(col(column).isin(value))
            else:
                # Equality condition
                filtered_df = filtered_df.filter(col(column) == value)

        return filtered_df

    def select_columns(self, df: DataFrame, columns: list[str]) -> DataFrame:
        """Select specific columns from DataFrame.

        Args:
            df: Input DataFrame
            columns: List of column names to select

        Returns:
            DataFrame with selected columns
        """
        return df.select(*[col(c) for c in columns])

    def add_column(
        self, df: DataFrame, column_name: str, expression: str
    ) -> DataFrame:
        """Add a new calculated column to DataFrame.

        Args:
            df: Input DataFrame
            column_name: Name of the new column
            expression: SQL expression for the column

        Returns:
            DataFrame with new column
        """
        return df.with_column(column_name, col(expression))

    def rename_columns(
        self, df: DataFrame, column_mapping: dict[str, str]
    ) -> DataFrame:
        """Rename columns in DataFrame.

        Args:
            df: Input DataFrame
            column_mapping: Dictionary mapping old names to new names

        Returns:
            DataFrame with renamed columns
        """
        renamed_df = df
        for old_name, new_name in column_mapping.items():
            renamed_df = renamed_df.with_column_renamed(old_name, new_name)
        return renamed_df

    def join_dataframes(
        self,
        left_df: DataFrame,
        right_df: DataFrame,
        join_type: str = "inner",
        on: str | None = None,
        left_on: str | None = None,
        right_on: str | None = None,
    ) -> DataFrame:
        """Join two DataFrames.

        Args:
            left_df: Left DataFrame
            right_df: Right DataFrame
            join_type: Type of join (inner, left, right, outer)
            on: Column name to join on (if same in both DataFrames)
            left_on: Left DataFrame column name
            right_on: Right DataFrame column name

        Returns:
            Joined DataFrame
        """
        if on:
            left_on = right_on = on

        if not left_on or not right_on:
            raise ValueError(
                "Must specify either 'on' or both 'left_on' and 'right_on'"
            )

        join_condition = col(left_on) == col(right_on)

        if join_type.lower() == "inner":
            return left_df.join(right_df, join_condition)
        elif join_type.lower() == "left":
            return left_df.join(right_df, join_condition, "left")
        elif join_type.lower() == "right":
            return left_df.join(right_df, join_condition, "right")
        elif join_type.lower() == "outer":
            return left_df.join(right_df, join_condition, "outer")
        else:
            raise ValueError(f"Unsupported join type: {join_type}")

    def aggregate_data(
        self, df: DataFrame, group_by: list[str], aggregations: dict[str, str]
    ) -> DataFrame:
        """Aggregate data by grouping columns.

        Args:
            df: Input DataFrame
            group_by: List of columns to group by
            aggregations: Dictionary of {column: aggregation_function}
                         Supported functions: count, sum, avg, max, min

        Returns:
            Aggregated DataFrame
        """
        agg_functions = {
            "count": count,
            "sum": sf_sum,
            "avg": avg,
            "max": sf_max,
            "min": sf_min,
        }

        agg_exprs = []
        for column, func_name in aggregations.items():
            if func_name not in agg_functions:
                raise ValueError(
                    f"Unsupported aggregation function: {func_name}"
                )

            agg_exprs.append(
                agg_functions[func_name](col(column)).alias(
                    f"{func_name}_{column}"
                )
            )

        return df.group_by(*[col(c) for c in group_by]).agg(*agg_exprs)

    def pivot_data(
        self,
        df: DataFrame,
        pivot_column: str,
        value_column: str,
        agg_function: str = "sum",
    ) -> DataFrame:
        """Pivot DataFrame on a column.

        Args:
            df: Input DataFrame
            pivot_column: Column to pivot on
            value_column: Column to aggregate
            agg_function: Aggregation function (sum, count, avg, etc.)

        Returns:
            Pivoted DataFrame
        """
        agg_functions = {
            "sum": sf_sum,
            "count": count,
            "avg": avg,
            "max": sf_max,
            "min": sf_min,
        }

        if agg_function not in agg_functions:
            raise ValueError(
                f"Unsupported aggregation function: {agg_function}"
            )

        return df.pivot(col(pivot_column)).agg(
            agg_functions[agg_function](col(value_column))
        )

    def sample_data(
        self, df: DataFrame, fraction: float = 0.1, method: str = "bernoulli"
    ) -> DataFrame:
        """Sample data from DataFrame.

        Args:
            df: Input DataFrame
            fraction: Fraction of data to sample (0.0 to 1.0)
            method: Sampling method (bernoulli, system)

        Returns:
            Sampled DataFrame
        """
        if not 0.0 < fraction <= 1.0:
            raise ValueError("Fraction must be between 0.0 and 1.0")

        if method not in ["bernoulli", "system"]:
            raise ValueError("Method must be 'bernoulli' or 'system'")

        return df.sample(fraction=fraction, method=method)

    def sort_data(
        self,
        df: DataFrame,
        columns: str | list[str],
        ascending: bool | list[bool] = True,
    ) -> DataFrame:
        """Sort DataFrame by columns.

        Args:
            df: Input DataFrame
            columns: Column name(s) to sort by
            ascending: Sort order (True for ascending, False for descending)

        Returns:
            Sorted DataFrame
        """
        if isinstance(columns, str):
            columns = [columns]

        if isinstance(ascending, bool):
            ascending = [ascending] * len(columns)
        elif len(ascending) != len(columns):
            raise ValueError(
                "Length of ascending must match length of columns"
            )

        sort_exprs = []
        for col_name, asc in zip(columns, ascending, strict=False):
            if asc:
                sort_exprs.append(col(col_name).asc())
            else:
                sort_exprs.append(col(col_name).desc())

        return df.sort(*sort_exprs)

    def limit_data(self, df: DataFrame, n: int) -> DataFrame:
        """Limit the number of rows in DataFrame.

        Args:
            df: Input DataFrame
            n: Maximum number of rows

        Returns:
            Limited DataFrame
        """
        return df.limit(n)

    def collect_data(self, df: DataFrame) -> list[dict[str, Any]]:
        """Collect DataFrame data to local Python list.

        Args:
            df: Input DataFrame

        Returns:
            List of dictionaries representing rows
        """
        try:
            result = df.collect()
            return [row.asDict() for row in result]
        except Exception as e:
            self._logger.error(f"Failed to collect data: {e}")
            raise SnowparkSQLException(f"Failed to collect data: {e}") from e

    def show_data(self, df: DataFrame, n: int = 10) -> None:
        """Display DataFrame data.

        Args:
            df: Input DataFrame
            n: Number of rows to display
        """
        df.show(n)

    def get_schema(self, df: DataFrame) -> list[dict[str, Any]]:
        """Get DataFrame schema information.

        Args:
            df: Input DataFrame

        Returns:
            List of column information dictionaries
        """
        schema = df.schema
        return [
            {
                "name": field.name,
                "type": str(field.datatype),
                "nullable": field.nullable,
            }
            for field in schema.fields
        ]

    def write_to_table(
        self,
        df: DataFrame,
        table_name: str,
        mode: str = "append",
        schema: str | None = None,
    ) -> None:
        """Write DataFrame to Snowflake table.

        Args:
            df: Input DataFrame
            table_name: Target table name
            mode: Write mode (append, overwrite, ignore)
            schema: Optional schema name
        """
        if schema:
            full_table_name = f"{schema}.{table_name}"
        else:
            full_table_name = table_name

        try:
            if mode == "append":
                df.write.mode("append").save_as_table(full_table_name)
            elif mode == "overwrite":
                df.write.mode("overwrite").save_as_table(full_table_name)
            elif mode == "ignore":
                df.write.mode("ignore").save_as_table(full_table_name)
            else:
                raise ValueError(f"Unsupported write mode: {mode}")

            self._logger.info(
                f"Successfully wrote data to table: {full_table_name}"
            )
        except Exception as e:
            self._logger.error(
                f"Failed to write to table {full_table_name}: {e}"
            )
            raise SnowparkSQLException(f"Failed to write to table: {e}") from e

    def __repr__(self) -> str:
        """String representation of the operations handler."""
        return f"SnowparkOperations(connection={self.connection is not None}, session={self.session is not None})"
