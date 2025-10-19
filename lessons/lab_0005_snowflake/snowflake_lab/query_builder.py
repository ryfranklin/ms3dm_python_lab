"""Query builder utilities for constructing SQL queries programmatically."""

import logging
from typing import Any

from snowflake.snowpark import DataFrame, Session
from snowflake.snowpark.exceptions import SnowparkSQLException

from .connection import SnowflakeConnection


class QueryBuilder:
    """Programmatic SQL query builder for Snowflake.

    This class provides a fluent interface for building complex SQL queries
    programmatically, making it easier to construct dynamic queries and
    avoid SQL injection vulnerabilities.
    """

    def __init__(self, connection: SnowflakeConnection | Session):
        """Initialize the query builder.

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
        self._reset()

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

    def _reset(self) -> None:
        """Reset the query builder state."""
        self._select_columns = []
        self._from_table = None
        self._joins = []
        self._where_conditions = []
        self._group_by_columns = []
        self._having_conditions = []
        self._order_by_columns = []
        self._limit_count = None
        self._offset_count = None

    def select(self, *columns: str | Any) -> "QueryBuilder":
        """Add columns to SELECT clause.

        Args:
            *columns: Column names or expressions

        Returns:
            QueryBuilder instance for method chaining
        """
        self._select_columns.extend(columns)
        return self

    def from_table(
        self,
        table_name: str,
        schema: str | None = None,
        alias: str | None = None,
    ) -> "QueryBuilder":
        """Set the FROM table.

        Args:
            table_name: Name of the table
            schema: Optional schema name
            alias: Optional table alias

        Returns:
            QueryBuilder instance for method chaining
        """
        if schema:
            full_table_name = f"{schema}.{table_name}"
        else:
            full_table_name = table_name

        if alias:
            self._from_table = f"{full_table_name} AS {alias}"
        else:
            self._from_table = full_table_name

        return self

    def join(
        self,
        table_name: str,
        condition: str,
        join_type: str = "INNER",
        schema: str | None = None,
        alias: str | None = None,
    ) -> "QueryBuilder":
        """Add a JOIN clause.

        Args:
            table_name: Name of the table to join
            condition: JOIN condition
            join_type: Type of join (INNER, LEFT, RIGHT, OUTER)
            schema: Optional schema name
            alias: Optional table alias

        Returns:
            QueryBuilder instance for method chaining
        """
        if schema:
            full_table_name = f"{schema}.{table_name}"
        else:
            full_table_name = table_name

        if alias:
            table_ref = f"{full_table_name} AS {alias}"
        else:
            table_ref = full_table_name

        self._joins.append(
            f"{join_type.upper()} JOIN {table_ref} ON {condition}"
        )
        return self

    def where(self, condition: str | Any) -> "QueryBuilder":
        """Add a WHERE condition.

        Args:
            condition: WHERE condition

        Returns:
            QueryBuilder instance for method chaining
        """
        self._where_conditions.append(condition)
        return self

    def group_by(self, *columns: str) -> "QueryBuilder":
        """Add columns to GROUP BY clause.

        Args:
            *columns: Column names to group by

        Returns:
            QueryBuilder instance for method chaining
        """
        self._group_by_columns.extend(columns)
        return self

    def aggregate(
        self, column: str, function: str, alias: str | None = None
    ) -> "QueryBuilder":
        """Add an aggregation to the SELECT clause.

        Args:
            column: Column to aggregate
            function: Aggregation function (count, sum, avg, max, min)
            alias: Optional alias for the aggregated column

        Returns:
            QueryBuilder instance for method chaining
        """
        if alias is None:
            alias = f"{function}_{column}"

        agg_expr = f"{function.upper()}({column}) AS {alias}"
        self._select_columns.append(agg_expr)
        return self

    def having(self, condition: str | Any) -> "QueryBuilder":
        """Add a HAVING condition.

        Args:
            condition: HAVING condition

        Returns:
            QueryBuilder instance for method chaining
        """
        self._having_conditions.append(condition)
        return self

    def order_by(self, column: str, ascending: bool = True) -> "QueryBuilder":
        """Add a column to ORDER BY clause.

        Args:
            column: Column name to order by
            ascending: Sort order (True for ASC, False for DESC)

        Returns:
            QueryBuilder instance for method chaining
        """
        direction = "ASC" if ascending else "DESC"
        self._order_by_columns.append(f"{column} {direction}")
        return self

    def limit(self, count: int) -> "QueryBuilder":
        """Add LIMIT clause.

        Args:
            count: Number of rows to limit

        Returns:
            QueryBuilder instance for method chaining
        """
        self._limit_count = count
        return self

    def offset(self, count: int) -> "QueryBuilder":
        """Add OFFSET clause.

        Args:
            count: Number of rows to skip

        Returns:
            QueryBuilder instance for method chaining
        """
        self._offset_count = count
        return self

    def build_sql(self) -> str:
        """Build the SQL query string.

        Returns:
            Complete SQL query string
        """
        if not self._select_columns:
            raise ValueError("SELECT clause is required")

        if not self._from_table:
            raise ValueError("FROM clause is required")

        # Build SELECT clause
        select_clause = "SELECT " + ", ".join(
            str(col) for col in self._select_columns
        )

        # Build FROM clause
        from_clause = f"FROM {self._from_table}"

        # Build JOIN clauses
        join_clause = ""
        if self._joins:
            join_clause = " " + " ".join(self._joins)

        # Build WHERE clause
        where_clause = ""
        if self._where_conditions:
            where_clause = " WHERE " + " AND ".join(
                str(cond) for cond in self._where_conditions
            )

        # Build GROUP BY clause
        group_by_clause = ""
        if self._group_by_columns:
            group_by_clause = " GROUP BY " + ", ".join(self._group_by_columns)

        # Build HAVING clause
        having_clause = ""
        if self._having_conditions:
            having_clause = " HAVING " + " AND ".join(
                str(cond) for cond in self._having_conditions
            )

        # Build ORDER BY clause
        order_by_clause = ""
        if self._order_by_columns:
            order_by_clause = " ORDER BY " + ", ".join(self._order_by_columns)

        # Build LIMIT clause
        limit_clause = ""
        if self._limit_count is not None:
            limit_clause = f" LIMIT {self._limit_count}"

        # Build OFFSET clause
        offset_clause = ""
        if self._offset_count is not None:
            offset_clause = f" OFFSET {self._offset_count}"

        # Combine all clauses
        sql = f"{select_clause} {from_clause}{join_clause}{where_clause}{group_by_clause}{having_clause}{order_by_clause}{limit_clause}{offset_clause}"

        return sql

    def execute(self) -> DataFrame:
        """Execute the built query.

        Returns:
            Snowpark DataFrame with query results
        """
        session = self._get_session()
        sql = self.build_sql()

        try:
            self._logger.info(f"Executing query: {sql}")
            df = session.sql(sql)
            return df
        except Exception as e:
            self._logger.error(f"Query execution failed: {e}")
            raise SnowparkSQLException(f"Query execution failed: {e}") from e

    def collect(self) -> list[dict[str, Any]]:
        """Execute the query and collect results.

        Returns:
            List of dictionaries representing rows
        """
        df = self.execute()
        return [row.asDict() for row in df.collect()]

    def show(self, n: int = 10) -> None:
        """Execute the query and show results.

        Args:
            n: Number of rows to display
        """
        df = self.execute()
        df.show(n)

    def count(self) -> int:
        """Execute the query and return the count of rows.

        Returns:
            Number of rows in the result
        """
        df = self.execute()
        return len(df.collect())

    def exists(self) -> bool:
        """Check if the query returns any rows.

        Returns:
            True if query returns at least one row, False otherwise
        """
        return self.count() > 0

    def first(self) -> dict[str, Any] | None:
        """Execute the query and return the first row.

        Returns:
            First row as dictionary, or None if no rows
        """
        df = self.execute()
        results = df.collect()
        return results[0].asDict() if results else None

    def __str__(self) -> str:
        """String representation of the query."""
        try:
            return self.build_sql()
        except ValueError as e:
            return f"QueryBuilder(incomplete: {e})"

    def __repr__(self) -> str:
        """Detailed string representation of the query builder."""
        return f"QueryBuilder(select={len(self._select_columns)}, from={self._from_table}, joins={len(self._joins)}, where={len(self._where_conditions)})"


class AnalyticsQueryBuilder(QueryBuilder):
    """Specialized query builder for analytics queries."""

    def __init__(self, connection: SnowflakeConnection | Session):
        """Initialize the analytics query builder.

        Args:
            connection: SnowflakeConnection or Snowpark Session
        """
        super().__init__(connection)
        self._aggregations = {}

    def aggregate(
        self, column: str, function: str, alias: str | None = None
    ) -> "AnalyticsQueryBuilder":
        """Add an aggregation to the query.

        Args:
            column: Column to aggregate
            function: Aggregation function (count, sum, avg, max, min)
            alias: Optional alias for the aggregated column

        Returns:
            AnalyticsQueryBuilder instance for method chaining
        """
        if alias is None:
            alias = f"{function}_{column}"

        self._aggregations[alias] = f"{function.upper()}({column})"
        return self

    def build_sql(self) -> str:
        """Build the SQL query string with aggregations.

        Returns:
            Complete SQL query string
        """
        if self._aggregations:
            # Add aggregations to SELECT clause
            agg_columns = [
                f"{expr} AS {alias}"
                for alias, expr in self._aggregations.items()
            ]
            self._select_columns.extend(agg_columns)

        return super().build_sql()

    def time_series_analysis(
        self,
        date_column: str,
        value_column: str,
        time_granularity: str = "DAY",
    ) -> "AnalyticsQueryBuilder":
        """Build a time series analysis query.

        Args:
            date_column: Column containing dates
            value_column: Column containing values to analyze
            time_granularity: Time granularity (DAY, WEEK, MONTH, QUARTER, YEAR)

        Returns:
            AnalyticsQueryBuilder instance for method chaining
        """
        # Add date truncation and grouping
        self.group_by(f"DATE_TRUNC('{time_granularity}', {date_column})")
        self.aggregate(value_column, "sum", f"total_{value_column}")
        self.aggregate(value_column, "avg", f"avg_{value_column}")
        self.aggregate(value_column, "count", f"count_{value_column}")
        self.order_by(f"DATE_TRUNC('{time_granularity}', {date_column})")

        return self

    def cohort_analysis(
        self, user_column: str, date_column: str, cohort_period: str = "MONTH"
    ) -> "AnalyticsQueryBuilder":
        """Build a cohort analysis query.

        Args:
            user_column: Column containing user identifiers
            date_column: Column containing dates
            cohort_period: Cohort period (DAY, WEEK, MONTH, QUARTER, YEAR)

        Returns:
            AnalyticsQueryBuilder instance for method chaining
        """
        # This is a simplified cohort analysis - in practice, you'd need more complex logic
        self.group_by(f"DATE_TRUNC('{cohort_period}', {date_column})")
        self.aggregate(user_column, "count", "cohort_size")
        self.aggregate(user_column, "count", "distinct_users")
        self.order_by(f"DATE_TRUNC('{cohort_period}', {date_column})")

        return self

    def funnel_analysis(
        self, step_columns: list[str], user_column: str
    ) -> "AnalyticsQueryBuilder":
        """Build a funnel analysis query.

        Args:
            step_columns: List of columns representing funnel steps
            user_column: Column containing user identifiers

        Returns:
            AnalyticsQueryBuilder instance for method chaining
        """
        # Add aggregations for each funnel step
        for i, step_col in enumerate(step_columns):
            self.aggregate(step_col, "count", f"step_{i + 1}_count")
            self.aggregate(user_column, "count", f"step_{i + 1}_users")

        return self
