#!/usr/bin/env python3
"""Basic Snowflake operations example.

This script demonstrates common Snowflake operations using the Snowflake Lab.
"""

import sys
from pathlib import Path

from snowflake_lab import (
    DataLoader,
    QueryBuilder,
    SnowflakeConnection,
    SnowparkOperations,
)

from core import get_logger, setup_logging

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Set up logging
setup_logging(level="INFO")
logger = get_logger(__name__)


def basic_dataframe_operations():
    """Demonstrate basic DataFrame operations."""
    logger.info("Basic DataFrame Operations")
    logger.info("=" * 40)

    try:
        # Create connection
        connection = SnowflakeConnection.from_environment()

        with connection.session_context() as session:
            ops = SnowparkOperations(session)

            # Create a sample DataFrame
            logger.info("Creating sample data...")
            sample_data = [
                {
                    "id": 1,
                    "name": "Alice",
                    "age": 30,
                    "department": "Engineering",
                },
                {"id": 2, "name": "Bob", "age": 25, "department": "Marketing"},
                {
                    "id": 3,
                    "name": "Charlie",
                    "age": 35,
                    "department": "Engineering",
                },
                {"id": 4, "name": "Diana", "age": 28, "department": "Sales"},
                {"id": 5, "name": "Eve", "age": 32, "department": "Marketing"},
            ]

            # Convert to DataFrame (using SQL for simplicity)
            df = session.create_dataframe(sample_data)

            logger.info("Sample data created")
            logger.info(f"Schema: {ops.get_schema(df)}")

            # Show the data
            logger.info("\nSample Data:")
            ops.show_data(df)

            # Filter data
            logger.info("\nFiltering data (age > 30):")
            filtered_df = ops.filter_data(
                df, {"age": (30, 100)}
            )  # Range filter
            ops.show_data(filtered_df)

            # Select specific columns
            logger.info("\nSelecting specific columns:")
            selected_df = ops.select_columns(df, ["name", "department"])
            ops.show_data(selected_df)

            # Add a calculated column
            logger.info("\nAdding calculated column:")
            with_calc_df = ops.add_column(
                df,
                "age_group",
                "CASE WHEN age < 30 THEN 'Young' ELSE 'Experienced' END",
            )
            ops.show_data(with_calc_df)

            # Aggregate data
            logger.info("\nAggregating data by department:")
            agg_df = ops.aggregate_data(
                df,
                group_by=["department"],
                aggregations={"age": "avg", "id": "count"},
            )
            ops.show_data(agg_df)

            # Sort data
            logger.info("\nSorting data by age (descending):")
            sorted_df = ops.sort_data(df, "age", ascending=False)
            ops.show_data(sorted_df)

            logger.info("\nBasic operations completed successfully!")

    except Exception as e:
        logger.error(f"Error in basic operations: {e}")
        raise


def query_builder_example():
    """Demonstrate the query builder."""
    logger.info("\nQuery Builder Example")
    logger.info("=" * 40)

    try:
        connection = SnowflakeConnection.from_environment()

        with connection.session_context() as session:
            # Create a sample table for demonstration
            logger.info("Creating sample table...")
            session.sql(
                """
                CREATE OR REPLACE TEMPORARY TABLE sample_employees AS
                SELECT * FROM VALUES
                    (1, 'Alice', 30, 'Engineering', 75000),
                    (2, 'Bob', 25, 'Marketing', 60000),
                    (3, 'Charlie', 35, 'Engineering', 85000),
                    (4, 'Diana', 28, 'Sales', 70000),
                    (5, 'Eve', 32, 'Marketing', 65000)
                AS t(id, name, age, department, salary)
            """
            ).collect()

            # Use query builder
            logger.info("Building query with QueryBuilder...")
            query = QueryBuilder(session)

            result = (
                query.select("name", "department", "salary")
                .from_table("sample_employees")
                .where("age > 30")
                .order_by("salary", ascending=False)
                .limit(3)
                .collect()
            )

            logger.info("Query executed successfully!")
            logger.info("Top 3 employees over 30 by salary:")
            for row in result:
                logger.info(
                    f"  {row['NAME']} - {row['DEPARTMENT']} - ${row['SALARY']:,}"
                )

            # Analytics query example
            logger.info("\nAnalytics Query Example:")
            analytics = QueryBuilder(session)

            analytics_result = (
                analytics.select("department")
                .from_table("sample_employees")
                .group_by("department")
                .aggregate("salary", "avg", "avg_salary")
                .aggregate("id", "count", "employee_count")
                .order_by("avg_salary", ascending=False)
                .collect()
            )

            logger.info("Department salary analysis:")
            for row in analytics_result:
                logger.info(
                    f"  {row['DEPARTMENT']}: {row['EMPLOYEE_COUNT']} employees, "
                    f"avg salary ${row['AVG_SALARY']:,.0f}"
                )

    except Exception as e:
        logger.error(f"Error in query builder example: {e}")
        raise


def data_loader_example():
    """Demonstrate data loading operations."""
    logger.info("\nData Loader Example")
    logger.info("=" * 40)

    try:
        connection = SnowflakeConnection.from_environment()

        with connection.session_context() as session:
            loader = DataLoader(session)

            # Create a table schema
            logger.info("Creating table schema...")
            schema_definition = [
                {"name": "id", "type": "INTEGER", "nullable": False},
                {"name": "name", "type": "VARCHAR(100)", "nullable": False},
                {"name": "age", "type": "INTEGER", "nullable": True},
                {
                    "name": "department",
                    "type": "VARCHAR(50)",
                    "nullable": True,
                },
                {"name": "salary", "type": "DECIMAL(10,2)", "nullable": True},
            ]

            loader.create_table_from_schema(
                "demo_employees", schema_definition, if_not_exists=True
            )

            logger.info("Table created successfully!")

            # Get table info
            table_info = loader.get_table_info("demo_employees")
            logger.info(
                f"Table info: {table_info['row_count']} rows, {len(table_info['columns'])} columns"
            )

            # Create sample data and load it
            logger.info("Creating and loading sample data...")
            sample_data = [
                {
                    "id": 1,
                    "name": "Alice",
                    "age": 30,
                    "department": "Engineering",
                    "salary": 75000.00,
                },
                {
                    "id": 2,
                    "name": "Bob",
                    "age": 25,
                    "department": "Marketing",
                    "salary": 60000.00,
                },
                {
                    "id": 3,
                    "name": "Charlie",
                    "age": 35,
                    "department": "Engineering",
                    "salary": 85000.00,
                },
            ]

            df = session.create_dataframe(sample_data)
            loader.load_from_dataframe(df, "demo_employees", mode="append")

            logger.info("Data loaded successfully!")

            # Verify the data
            ops = SnowparkOperations(session)
            loaded_df = ops.read_table("demo_employees")
            logger.info("Loaded data:")
            ops.show_data(loaded_df)

    except Exception as e:
        logger.error(f"Error in data loader example: {e}")
        raise


def main():
    """Main function to run all examples."""
    logger.info("Snowflake Lab - Basic Operations Demo")
    logger.info("=" * 50)

    try:
        # Test connection first
        connection = SnowflakeConnection.from_environment()
        if not connection.test_connection():
            logger.error(
                "Connection test failed. Please check your configuration."
            )
            return False

        # Run examples
        basic_dataframe_operations()
        query_builder_example()
        data_loader_example()

        logger.info("\nAll examples completed successfully!")

        return True

    except Exception as e:
        logger.error(f"Error running examples: {e}")
        return False

    finally:
        try:
            connection.close_all_sessions()
        except:
            pass


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
