# Lab 0005: Snowflake + Snowpark Integration

**Status**: ✅ Complete
**Difficulty**: Intermediate to Advanced
**Concepts**: Data Engineering, Snowpark, DataFrame Operations, ETL Patterns, Key-Pair Authentication

## 🎯 Learning Objectives

By the end of this lab, you will understand:

- ✅ How to connect to Snowflake using key-pair authentication
- ✅ How to work with Snowpark DataFrames for data processing
- ✅ How to build ETL pipelines and data loading workflows
- ✅ How to use programmatic query builders for complex SQL
- ✅ How to integrate with lab_0002 config loader for secure credential management
- ✅ How to prepare for AI agent integration (lab_0004) for data analytics

## 📚 What is Snowpark?

**Snowpark** is Snowflake's developer framework that allows you to build data applications using familiar programming languages like Python. It provides:

- **DataFrame API**: Similar to pandas but optimized for Snowflake's cloud data platform
- **Lazy Evaluation**: Queries are optimized and executed efficiently in Snowflake
- **Python Integration**: Use familiar Python libraries and patterns
- **Scalability**: Automatically scales with your data size

This lab provides a comprehensive toolkit for working with Snowflake using Snowpark, including connection management, data operations, and ETL patterns.

## 🏗️ Architecture

This lab implements a complete Snowflake integration system:

### 1. **Configuration Management** (`config.py`)

- Uses lab_0002 config loader for secure credential management
- Supports both key-pair and password authentication
- **Pydantic V2 validation** for type safety and performance
- Environment variable support with automatic resolution
- **Updated field validation** using `@field_validator` decorators

### 2. **Connection Management** (`connection.py`)

- Connection pooling and session management
- Automatic reconnection and error handling
- Context managers for resource cleanup
- Support for multiple concurrent sessions

### 3. **DataFrame Operations** (`dataframe_operations.py`)

- High-level operations for common data transformations
- Filtering, selecting, joining, and aggregating data
- Schema inspection and data validation
- Write operations to Snowflake tables

### 4. **Data Loading** (`data_loader.py`)

- ETL utilities for loading data from various sources
- Support for CSV, JSON, and Parquet files
- Table creation and management
- Data copying and transformation

### 5. **Query Builder** (`query_builder.py`)

- Programmatic SQL query construction
- Fluent interface for complex queries
- Analytics-specific query patterns
- SQL injection protection

## 🚀 Quick Start

### Prerequisites

1. **Snowflake Account**: You need access to a Snowflake account
2. **Python Environment**: Python 3.13+ with required dependencies
3. **Key Pair Authentication**: RSA key pair for secure authentication

### Installation

```bash
# From the repository root
cd lessons/lab_0005_snowflake

# Install dependencies (if not already installed)
pip install -e ".[dev]"

# Note: This lab uses Pydantic V2 for enhanced performance and validation
# All configuration models are updated to use the latest Pydantic features
```

### Setup Snowflake User

1. **Run the setup script** in Snowflake as ACCOUNTADMIN:

```sql
-- Run this in Snowflake
\@examples/setup_snowflake_user.sql
```

1. **Generate your key pair** (if you haven't already):

```bash
# Generate private key
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out snowflake_rsa_key.pem -nocrypt

# Extract public key
openssl rsa -in snowflake_rsa_key.pem -pubout -out snowflake_rsa_key.pub
```

2. **Update the SQL script** with your public key and run it in Snowflake.

### Configuration

3. **Copy the environment template**:

```bash
cp examples/snowflake.env.template .env
```

4. **Edit `.env`** with your Snowflake details:

```bash
# Snowflake Connection
SNOWFLAKE_ACCOUNT=your_account.us-east-1
SNOWFLAKE_USER=YOUR_USERNAME
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=ANALYTICS
SNOWFLAKE_SCHEMA=PUBLIC
SNOWFLAKE_ROLE=YOUR_ROLE

# Key Pair Authentication
SNOWFLAKE_PRIVATE_KEY_PATH=/path/to/your/snowflake_rsa_key.pem
```

5. **Test your connection**:

```bash
python examples/test_connection.py
```

### Basic Usage

```python
from snowflake_lab import SnowflakeConnection, SnowparkOperations

# Connect to Snowflake
connection = SnowflakeConnection.from_environment()

# Work with DataFrames
with connection.session_context() as session:
    ops = SnowparkOperations(session)

    # Read data
    df = ops.read_table("my_table")

    # Transform data
    filtered_df = ops.filter_data(df, {"age": (25, 65)})
    result = ops.aggregate_data(filtered_df, ["department"], {"salary": "avg"})

    # Show results
    ops.show_data(result)
```

## 🔍 Key Features

### 1. **Secure Authentication**

```python
# Key-pair authentication (recommended)
config = SnowflakeConfig(
    account="your_account.us-east-1",
    user="YOUR_USERNAME",
    private_key_path="/path/to/private_key.pem"
)

# Or password authentication
config = SnowflakeConfig(
    account="your_account.us-east-1",
    user="YOUR_USERNAME",
    password="your_password"
)

# Note: All configuration models use Pydantic V2 with enhanced validation
# Field names have been updated (e.g., 'schema' → 'schema_name') to avoid conflicts
```

### 2. **DataFrame Operations**

```python
# Filter data
filtered_df = ops.filter_data(df, {
    "age": (25, 65),  # Range filter
    "department": ["Engineering", "Marketing"]  # IN filter
})

# Join DataFrames
joined_df = ops.join_dataframes(
    employees_df, departments_df,
    join_type="left", left_on="dept_id", right_on="id"
)

# Aggregate data
agg_df = ops.aggregate_data(
    df,
    group_by=["department", "year"],
    aggregations={"salary": "avg", "id": "count"}
)
```

### 3. **Query Builder**

```python
# Build complex queries programmatically
query = QueryBuilder(session)
result = (query
    .select("name", "department", "salary")
    .from_table("employees")
    .join("departments", "employees.dept_id = departments.id")
    .where("salary > 50000")
    .group_by("department")
    .order_by("salary", ascending=False)
    .limit(10)
    .collect())
```

### 4. **Data Loading**

```python
# Load from file
loader = DataLoader(session)
loader.load_from_file(
    "data.csv",
    "employees",
    file_format="csv",
    mode="append"
)

# Load from DataFrame
loader.load_from_dataframe(df, "employees", mode="overwrite")
```

### 5. **Analytics Queries**

```python
# Time series analysis
analytics = AnalyticsQueryBuilder(session)
time_series = (analytics
    .from_table("sales")
    .time_series_analysis("sale_date", "amount", "MONTH")
    .collect())

# Cohort analysis
cohorts = (analytics
    .from_table("user_events")
    .cohort_analysis("user_id", "event_date", "MONTH")
    .collect())
```

## 🧪 Running Tests

This lab includes comprehensive test coverage:

```bash
# Run all tests
pytest

# Run specific test modules
pytest tests/test_config.py
pytest tests/test_connection.py

# Run with coverage
pytest --cov=snowflake_lab --cov-report=term-missing

# Run with verbose output
pytest -v
```

Test coverage includes:

- ✅ Configuration management and validation
- ✅ Connection management and pooling
- ✅ DataFrame operations and transformations
- ✅ Data loading and ETL operations
- ✅ Query builder functionality
- ✅ Error handling and edge cases

## 💡 Examples

### Example 1: Basic Data Analysis

```python
from snowflake_lab import SnowflakeConnection, SnowparkOperations

# Connect and analyze data
with SnowflakeConnection.from_environment() as conn:
    with conn.session_context() as session:
        ops = SnowparkOperations(session)

        # Read sales data
        sales_df = ops.read_table("sales")

        # Analyze by product category
        analysis = ops.aggregate_data(
            sales_df,
            group_by=["product_category"],
            aggregations={"amount": "sum", "order_id": "count"}
        )

        # Show top categories
        top_categories = ops.sort_data(analysis, "sum_amount", ascending=False)
        ops.show_data(top_categories, n=5)
```

### Example 2: ETL Pipeline

```python
from snowflake_lab import SnowflakeConnection, DataLoader

# ETL pipeline
with SnowflakeConnection.from_environment() as conn:
    with conn.session_context() as session:
        loader = DataLoader(session)

        # Create target table
        schema = [
            {"name": "id", "type": "INTEGER", "nullable": False},
            {"name": "name", "type": "VARCHAR(100)", "nullable": False},
            {"name": "email", "type": "VARCHAR(255)", "nullable": True},
        ]
        loader.create_table_from_schema("users", schema)

        # Load data from CSV
        loader.load_from_file(
            "users.csv",
            "users",
            file_format="csv",
            mode="append"
        )

        # Verify load
        info = loader.get_table_info("users")
        print(f"Loaded {info['row_count']} users")
```

### Example 3: Analytics Dashboard

```python
from snowflake_lab import SnowflakeConnection, AnalyticsQueryBuilder

# Build analytics queries
with SnowflakeConnection.from_environment() as conn:
    with conn.session_context() as session:
        analytics = AnalyticsQueryBuilder(session)

        # Revenue trends
        revenue_trends = (analytics
            .from_table("orders")
            .time_series_analysis("order_date", "total_amount", "MONTH")
            .collect())

        # Customer cohorts
        customer_cohorts = (analytics
            .from_table("customer_orders")
            .cohort_analysis("customer_id", "first_order_date", "MONTH")
            .collect())

        # Product funnel
        product_funnel = (analytics
            .from_table("user_events")
            .funnel_analysis(["viewed", "added_to_cart", "purchased"], "user_id")
            .collect())
```

## 🤖 AI Integration Path (Lab 0004)

This lab is designed to integrate seamlessly with lab_0004 AI agents for data analytics:

### Natural Language to SQL

```python
# Future integration with AI agent
from lab_0004_ai_agent import LLMClient

def natural_language_query(question: str):
    """Convert natural language to SQL using AI."""
    llm_client = LLMClient()

    prompt = f"""
    Convert this natural language question to SQL:
    Question: {question}

    Available tables: employees, departments, sales
    Use Snowflake SQL syntax.
    """

    sql_query = llm_client.chat(
        system_prompt="You are a SQL expert specializing in Snowflake.",
        user_message=prompt
    )

    # Execute the generated query
    with SnowflakeConnection.from_environment() as conn:
        with conn.session_context() as session:
            ops = SnowparkOperations(session)
            return ops.read_sql(sql_query).collect()
```

### Data Analytics Bot

```python
# Future: Complete analytics bot
class DataAnalyticsBot:
    def __init__(self):
        self.llm_client = LLMClient()
        self.snowflake_conn = SnowflakeConnection.from_environment()

    def analyze_data(self, question: str):
        """Answer data questions using AI + Snowflake."""
        # Generate SQL from natural language
        sql = self.generate_sql(question)

        # Execute query
        with self.snowflake_conn.session_context() as session:
            ops = SnowparkOperations(session)
            data = ops.read_sql(sql).collect()

        # Generate insights using AI
        insights = self.generate_insights(question, data)
        return insights
```

## 🌟 Real-World Applications

Snowflake + Snowpark is used in:

1. **Data Engineering**: ETL pipelines, data warehousing, data lakes
2. **Analytics**: Business intelligence, reporting, dashboards
3. **Machine Learning**: Feature engineering, model training, inference
4. **Data Science**: Exploratory data analysis, statistical modeling
5. **Application Development**: Data-driven applications and APIs

## 🚀 Pydantic V2 Migration

This lab has been fully migrated to **Pydantic V2** for enhanced performance and validation:

### **Key Changes Made:**

1. **Updated Field Validators:**

   ```python
   # Old Pydantic V1 style
   @validator("field_name")
   def validate_field(cls, v):
       return v

   # New Pydantic V2 style
   @field_validator("field_name")
   @classmethod
   def validate_field(cls, v):
       return v
   ```

2. **Updated Method Names:**

   ```python
   # Old: config.dict()
   # New: config.model_dump()
   ```

3. **Fixed Field Shadowing:**
   - Renamed `schema` field to `schema_name` to avoid shadowing Pydantic's built-in `schema` method
   - Updated all configuration files and references accordingly

4. **Enhanced Environment Variable Resolution:**
   - Automatic loading of `.env` files
   - Support for `${VARIABLE}` substitution in YAML configurations
   - Improved error handling and validation

### **Benefits:**

- ✅ **Better Performance**: Pydantic V2 is significantly faster
- ✅ **Enhanced Validation**: More robust type checking and error messages
- ✅ **Future-Proof**: Uses the latest Pydantic features and patterns
- ✅ **No Warnings**: Clean execution without deprecation warnings

## 🔧 Troubleshooting

### Common Issues

#### 1. Connection Failed

```text
SnowparkSQLException: Connection failed: Authentication failed
```

**Solution**: Check your account identifier, user credentials, and key file path.

#### 2. Key Pair Authentication Error

```text
ValueError: Failed to load private key
```

**Solution**: Ensure your private key file exists and is in PEM format.

#### 3. Permission Denied

```text
SnowparkSQLException: Insufficient privileges
```

**Solution**: Verify your user has the correct role and permissions in Snowflake.

#### 4. Table Not Found

```text
SnowparkSQLException: Table not found
```

**Solution**: Check table name, schema, and database. Ensure you're using the correct case.

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Your Snowflake code here
```

## 📖 Further Reading

- [Snowpark Python Documentation](https://docs.snowflake.com/en/developer-guide/snowpark/python/index.html) - Official Snowpark docs
- [Snowflake SQL Reference](https://docs.snowflake.com/en/sql-reference/index.html) - SQL syntax and functions
- [Snowflake Best Practices](https://docs.snowflake.com/en/user-guide/best-practices.html) - Performance optimization
- [Data Engineering Patterns](https://martinfowler.com/articles/data-mesh-principles.html) - Modern data architecture

## 🎓 Teaching Notes

This lab is ideal for:

- **Data Engineering Course**: ETL patterns, data warehousing
- **Analytics Workshop**: Business intelligence, reporting
- **Python for Data Science**: Advanced data processing
- **Cloud Computing**: Modern data platform architecture

**Estimated time**: 4-6 hours for complete implementation and testing

**Prerequisites**: Basic Python knowledge, understanding of SQL, familiarity with data concepts

---

[← Back to Main README](../../README.md) | [View Examples →](./examples/basic_operations.py) | [Test Connection →](./examples/test_connection.py)
