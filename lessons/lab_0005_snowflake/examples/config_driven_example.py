#!/usr/bin/env python3
"""
Configuration-Driven Snowflake Example

This example demonstrates how to use the lab_0002 config loader
to manage Snowflake operations with a complete environment setup.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from core import get_logger, setup_logging
from lessons.lab_0005_snowflake.snowflake_lab import (
    DataLoader,
    QueryBuilder,
    SnowflakeConfigSetup,
    SnowflakeConnection,
)

# Set up logging
setup_logging(level="INFO")
logger = get_logger(__name__)


def setup_environment():
    """Set up the Snowflake environment using configuration."""
    logger.info("Setting up Snowflake environment...")

    config_file = Path(__file__).parent / "snowflake_environment.yaml"
    setup = SnowflakeConfigSetup(str(config_file))

    results = setup.setup_environment()

    if "error" in results:
        logger.error(f"Setup failed: {results['error']}")
        return False

    logger.info("Environment setup completed!")
    return True


def load_sample_data():
    """Load sample data into the configured tables."""
    print("\n📊 Loading sample data...")

    try:
        # Connect using the configuration
        connection = SnowflakeConnection.from_environment()

        with connection.session_context() as session:
            loader = DataLoader(session)

            # Load employee data
            print("👥 Loading employee data...")
            employee_data = [
                {
                    "ID": 1,
                    "NAME": "Alice Johnson",
                    "AGE": 30,
                    "DEPARTMENT": "Engineering",
                    "SALARY": 75000.00,
                    "HIRE_DATE": "2020-01-15",
                    "IS_ACTIVE": True,
                },
                {
                    "ID": 2,
                    "NAME": "Bob Smith",
                    "AGE": 25,
                    "DEPARTMENT": "Marketing",
                    "SALARY": 60000.00,
                    "HIRE_DATE": "2021-03-20",
                    "IS_ACTIVE": True,
                },
                {
                    "ID": 3,
                    "NAME": "Charlie Brown",
                    "AGE": 35,
                    "DEPARTMENT": "Engineering",
                    "SALARY": 85000.00,
                    "HIRE_DATE": "2019-06-10",
                    "IS_ACTIVE": True,
                },
                {
                    "ID": 4,
                    "NAME": "Diana Prince",
                    "AGE": 28,
                    "DEPARTMENT": "Sales",
                    "SALARY": 70000.00,
                    "HIRE_DATE": "2020-09-05",
                    "IS_ACTIVE": True,
                },
                {
                    "ID": 5,
                    "NAME": "Eve Wilson",
                    "AGE": 32,
                    "DEPARTMENT": "Marketing",
                    "SALARY": 65000.00,
                    "HIRE_DATE": "2021-01-12",
                    "IS_ACTIVE": False,
                },
            ]

            df_employees = session.create_dataframe(employee_data)
            loader.load_from_dataframe(
                df_employees, "EMPLOYEES", mode="overwrite"
            )
            print("✅ Employee data loaded")

            # Load sales data
            print("💰 Loading sales data...")
            sales_data = [
                {
                    "SALE_ID": 1,
                    "PRODUCT_NAME": "Laptop Pro",
                    "QUANTITY": 2,
                    "UNIT_PRICE": 1200.00,
                    "TOTAL_AMOUNT": 2400.00,
                    "SALE_DATE": "2023-01-15",
                    "SALES_REP_ID": 1,
                },
                {
                    "SALE_ID": 2,
                    "PRODUCT_NAME": "Wireless Mouse",
                    "QUANTITY": 5,
                    "UNIT_PRICE": 25.00,
                    "TOTAL_AMOUNT": 125.00,
                    "SALE_DATE": "2023-01-16",
                    "SALES_REP_ID": 2,
                },
                {
                    "SALE_ID": 3,
                    "PRODUCT_NAME": "Monitor 4K",
                    "QUANTITY": 1,
                    "UNIT_PRICE": 400.00,
                    "TOTAL_AMOUNT": 400.00,
                    "SALE_DATE": "2023-01-17",
                    "SALES_REP_ID": 1,
                },
                {
                    "SALE_ID": 4,
                    "PRODUCT_NAME": "Keyboard",
                    "QUANTITY": 3,
                    "UNIT_PRICE": 80.00,
                    "TOTAL_AMOUNT": 240.00,
                    "SALE_DATE": "2023-01-18",
                    "SALES_REP_ID": 3,
                },
                {
                    "SALE_ID": 5,
                    "PRODUCT_NAME": "Laptop Pro",
                    "QUANTITY": 1,
                    "UNIT_PRICE": 1200.00,
                    "TOTAL_AMOUNT": 1200.00,
                    "SALE_DATE": "2023-01-19",
                    "SALES_REP_ID": 2,
                },
            ]

            df_sales = session.create_dataframe(sales_data)
            loader.load_from_dataframe(
                df_sales, "SALES_DATA", mode="overwrite"
            )
            print("✅ Sales data loaded")

            # Load product data
            print("📦 Loading product data...")
            product_data = [
                {
                    "PRODUCT_ID": 1,
                    "PRODUCT_NAME": "Laptop Pro",
                    "CATEGORY": "Computers",
                    "SUPPLIER": "TechCorp",
                    "UNIT_COST": 800.00,
                    "STOCK_QUANTITY": 50,
                },
                {
                    "PRODUCT_ID": 2,
                    "PRODUCT_NAME": "Wireless Mouse",
                    "CATEGORY": "Accessories",
                    "SUPPLIER": "AccessoryInc",
                    "UNIT_COST": 15.00,
                    "STOCK_QUANTITY": 200,
                },
                {
                    "PRODUCT_ID": 3,
                    "PRODUCT_NAME": "Monitor 4K",
                    "CATEGORY": "Displays",
                    "SUPPLIER": "DisplayTech",
                    "UNIT_COST": 250.00,
                    "STOCK_QUANTITY": 30,
                },
                {
                    "PRODUCT_ID": 4,
                    "PRODUCT_NAME": "Keyboard",
                    "CATEGORY": "Accessories",
                    "SUPPLIER": "AccessoryInc",
                    "UNIT_COST": 50.00,
                    "STOCK_QUANTITY": 100,
                },
            ]

            df_products = session.create_dataframe(product_data)
            loader.load_from_dataframe(
                df_products, "PRODUCTS", mode="overwrite"
            )
            print("✅ Product data loaded")

    except Exception as e:
        print(f"❌ Error loading sample data: {e}")
        return False

    return True


def run_analytics_queries():
    """Run analytics queries using the loaded data."""
    print("\n📈 Running analytics queries...")

    try:
        connection = SnowflakeConnection.from_environment()

        with connection.session_context() as session:
            query = QueryBuilder(session)

            # Query 1: Employee summary by department
            print("\n👥 Employee Summary by Department:")
            print("-" * 50)

            dept_summary = (
                query.select("DEPARTMENT")
                .from_table("PYTHON_LEARNING_LAB.EXAMPLES.EMPLOYEES")
                .group_by("DEPARTMENT")
                .aggregate("ID", "count", "employee_count")
                .aggregate("SALARY", "avg", "avg_salary")
                .aggregate("AGE", "avg", "avg_age")
                .order_by("avg_salary", ascending=False)
                .collect()
            )

            for row in dept_summary:
                print(
                    f"{row['DEPARTMENT']:15} | {row['EMPLOYEE_COUNT']:2} employees | "
                    f"Avg Salary: ${row['AVG_SALARY']:8,.0f} | Avg Age: {row['AVG_AGE']:4.1f}"
                )

            # Query 2: Sales performance
            print("\n💰 Sales Performance:")
            print("-" * 50)

            sales_performance = (
                query.select("PRODUCT_NAME", "TOTAL_AMOUNT", "SALE_DATE")
                .from_table("PYTHON_LEARNING_LAB.EXAMPLES.SALES_DATA")
                .order_by("TOTAL_AMOUNT", ascending=False)
                .limit(5)
                .collect()
            )

            for row in sales_performance:
                print(
                    f"{row['PRODUCT_NAME']:20} | ${row['TOTAL_AMOUNT']:8,.2f} | {row['SALE_DATE']}"
                )

            # Query 3: Product profitability
            print("\n📊 Product Profitability Analysis:")
            print("-" * 50)

            profitability_sql = """
            SELECT
                p.PRODUCT_NAME,
                p.UNIT_COST,
                AVG(s.UNIT_PRICE) as avg_selling_price,
                AVG(s.UNIT_PRICE) - p.UNIT_COST as profit_per_unit,
                SUM(s.QUANTITY) as total_sold,
                SUM(s.TOTAL_AMOUNT) as total_revenue
            FROM PYTHON_LEARNING_LAB.EXAMPLES.PRODUCTS p
            JOIN PYTHON_LEARNING_LAB.EXAMPLES.SALES_DATA s ON p.PRODUCT_NAME = s.PRODUCT_NAME
            GROUP BY p.PRODUCT_NAME, p.UNIT_COST
            ORDER BY profit_per_unit DESC
            """

            profitability = session.sql(profitability_sql).collect()

            for row in profitability:
                print(
                    f"{row['PRODUCT_NAME']:20} | Cost: ${row['UNIT_COST']:6.2f} | "
                    f"Avg Price: ${row['AVG_SELLING_PRICE']:6.2f} | "
                    f"Profit: ${row['PROFIT_PER_UNIT']:6.2f} | "
                    f"Revenue: ${row['TOTAL_REVENUE']:8,.2f}"
                )

            # Query 4: Active vs Inactive employees
            print("\n👤 Employee Status Analysis:")
            print("-" * 50)

            status_analysis = (
                query.select("IS_ACTIVE")
                .from_table("PYTHON_LEARNING_LAB.EXAMPLES.EMPLOYEES")
                .group_by("IS_ACTIVE")
                .aggregate("ID", "count", "count")
                .collect()
            )

            for row in status_analysis:
                status = "Active" if row["IS_ACTIVE"] else "Inactive"
                print(f"{status:8} employees: {row['COUNT']:2}")

    except Exception as e:
        print(f"❌ Error running analytics queries: {e}")
        return False

    return True


def demonstrate_config_usage():
    """Demonstrate how to use configuration in various operations."""
    print("\n⚙️  Configuration Usage Examples:")
    print("-" * 50)

    try:
        # Load configuration using lab_0002 config loader
        from lessons.lab_0002_config_loader.config_loader import ConfigManager

        config_file = Path(__file__).parent / "snowflake_environment.yaml"
        config = ConfigManager.load_from_file(str(config_file))

        # Access configuration values
        print("📋 Configuration Values:")
        print(f"  Database: {config.get('environment.database.name')}")
        print(f"  Schema: {config.get('environment.schema.name')}")
        print(f"  Warehouse: {config.get('environment.warehouse.name')}")
        print(f"  Project: {config.get('project.name')}")
        print(f"  Version: {config.get('project.version')}")

        # Show table configurations
        tables = config.get("environment.tables", [])
        print(f"\n📊 Configured Tables ({len(tables)}):")
        for table in tables:
            columns = len(table.get("columns", []))
            print(f"  - {table['name']} ({columns} columns)")

        # Show role configurations
        roles = config.get("environment.roles", [])
        print(f"\n🔐 Configured Roles ({len(roles)}):")
        for role in roles:
            print(f"  - {role['name']}")

    except Exception as e:
        print(f"❌ Error demonstrating config usage: {e}")
        return False

    return True


def main():
    """Main function."""
    print("❄️  Configuration-Driven Snowflake Example")
    print("=" * 60)

    try:
        # Step 1: Set up environment
        if not setup_environment():
            print("❌ Environment setup failed")
            return False

        # Step 2: Load sample data
        if not load_sample_data():
            print("❌ Data loading failed")
            return False

        # Step 3: Run analytics
        if not run_analytics_queries():
            print("❌ Analytics queries failed")
            return False

        # Step 4: Demonstrate config usage
        if not demonstrate_config_usage():
            print("❌ Config demonstration failed")
            return False

        print("\n🎉 All examples completed successfully!")
        print("🚀 Your Snowflake environment is ready for development!")

        return True

    except Exception as e:
        print(f"❌ Example failed: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
