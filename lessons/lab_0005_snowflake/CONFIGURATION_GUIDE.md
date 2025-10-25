# Snowflake Lab Configuration Guide

This guide explains how to use the lab_0002 config loader to manage your Snowflake environment with comprehensive configuration-driven setup.

## 🎯 Overview

The Snowflake Lab now includes a complete configuration system that allows you to:

- Define your entire Snowflake environment in YAML/JSON/TOML files
- Automatically create databases, schemas, warehouses, roles, and users
- Load sample data and set up tables
- Manage permissions and grants
- Use the same configuration across different environments

## 📁 Configuration Files

### 1. Environment Configuration (`snowflake_environment.yaml`)

This is the main configuration file that defines your complete Snowflake environment:

```yaml
# Connection settings (can also use .env file)
connection:
  account: "${SNOWFLAKE_ACCOUNT}"
  user: "${SNOWFLAKE_USER}"
  private_key_path: "${SNOWFLAKE_PRIVATE_KEY_PATH}"
  # ... other connection parameters

# Environment setup
environment:
  database:
    name: "PYTHON_LEARNING_LAB"
    comment: "Database for Python Learning Lab"
    # ... other database settings

  schema:
    schema_name: "EXAMPLES"
    database: "PYTHON_LEARNING_LAB"
    # ... other schema settings

  tables:
    - name: "EMPLOYEES"
      schema_name: "EXAMPLES"
      database: "PYTHON_LEARNING_LAB"
      columns:
        - name: "ID"
          type: "INTEGER"
          nullable: false
        # ... more columns
```

### 2. Environment Variables (`.env`)

Create a `.env` file with your Snowflake credentials:

```bash
# Snowflake Connection
SNOWFLAKE_ACCOUNT=your_account_identifier
SNOWFLAKE_USER=YOUR_USERNAME
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=PYTHON_LEARNING_LAB
SNOWFLAKE_SCHEMA=EXAMPLES
SNOWFLAKE_ROLE=YOUR_ROLE

# Key Pair Authentication
SNOWFLAKE_PRIVATE_KEY_PATH=/path/to/your/private_key.pem
SNOWFLAKE_PRIVATE_KEY_PASSPHRASE=your_passphrase_if_encrypted
```

## 🚀 Quick Start

### 1. Set Up Your Environment

```bash
# Navigate to the examples directory
cd lessons/lab_0005_snowflake/examples

# Copy the environment template
cp snowflake.env.template .env

# Edit .env with your actual Snowflake credentials
# Then run the setup script
python setup_environment.py
```

### 2. Run the Configuration-Driven Example

```bash
# Run the comprehensive example
python config_driven_example.py
```

### 3. Verify Your Setup

```bash
# Verify the environment was created correctly
python setup_environment.py --verify-only
```

## 🔧 Configuration Components

### Database Configuration

```yaml
database:
  name: "PYTHON_LEARNING_LAB"
  if_not_exists: true
  comment: "Database for Python Learning Lab"
  data_retention_time_in_days: 1
  owner: "YOUR_ROLE"
```

### Schema Configuration

```yaml
schema:
  schema_name: "EXAMPLES"
  database: "PYTHON_LEARNING_LAB"
  if_not_exists: true
  comment: "Schema for examples"
  managed_access: false
  owner: "YOUR_ROLE"
```

### Warehouse Configuration

```yaml
warehouse:
  name: "PYTHON_LAB_WH"
  if_not_exists: true
  size: "X-SMALL"
  auto_suspend: 60
  auto_resume: true
  comment: "Warehouse for Python lab"
  owner: "YOUR_ROLE"
```

### Table Configuration

```yaml
tables:
  - name: "EMPLOYEES"
    schema_name: "EXAMPLES"
    database: "PYTHON_LEARNING_LAB"
    if_not_exists: true
    comment: "Employee data table"
    columns:
      - name: "ID"
        type: "INTEGER"
        nullable: false
        comment: "Employee ID"
      - name: "NAME"
        type: "VARCHAR(100)"
        nullable: false
        comment: "Employee name"
      # ... more columns
```

### Role and User Configuration

```yaml
roles:
  - name: "PYTHON_LAB_READER"
    if_not_exists: true
    comment: "Read-only role for examples"
    owner: "YOUR_ROLE"

users:
  - name: "PYTHON_LAB_DEMO"
    if_not_exists: true
    display_name: "Python Lab Demo User"
    email: "demo@pythonlearninglab.com"
    default_role: "PYTHON_LAB_READER"
    default_warehouse: "PYTHON_LAB_WH"
    comment: "Demo user for examples"
```

### Grant Configuration

```yaml
grants:
  - sql: "GRANT USAGE ON DATABASE PYTHON_LEARNING_LAB TO ROLE PYTHON_LAB_READER;"
  - sql: "GRANT USAGE ON SCHEMA PYTHON_LEARNING_LAB.EXAMPLES TO ROLE PYTHON_LAB_READER;"
  - sql: "GRANT SELECT ON ALL TABLES IN SCHEMA PYTHON_LEARNING_LAB.EXAMPLES TO ROLE PYTHON_LAB_READER;"
```

## 🛠️ Using the Configuration System

### 1. Programmatic Setup

```python
from snowflake_lab import SnowflakeConfigSetup

# Set up environment from configuration
setup = SnowflakeConfigSetup("snowflake_environment.yaml")
results = setup.setup_environment()

# Check results
if results.get("database"):
    print("✅ Database created successfully")
```

### 2. Using Configuration in Your Code

```python
from lessons.lab_0002_config_loader.config_loader import ConfigManager
from snowflake_lab import SnowflakeConnection

# Load configuration
config = ConfigManager.load_from_file("snowflake_environment.yaml")

# Get database and schema names
database = config.get("environment.database.name")
schema = config.get("environment.schema.name")

# Connect using configuration
connection = SnowflakeConnection.from_environment()
with connection.session_context() as session:
    # Use the configured database and schema
    df = session.table(f"{database}.{schema}.EMPLOYEES")
```

### 3. Environment-Specific Configurations

You can create different configuration files for different environments:

```bash
# Development environment
snowflake_environment_dev.yaml

# Production environment
snowflake_environment_prod.yaml

# Testing environment
snowflake_environment_test.yaml
```

## 📊 Sample Data

The configuration system includes sample data for:

- **EMPLOYEES**: Employee information with departments and salaries
- **SALES_DATA**: Sales transactions with products and amounts
- **PRODUCTS**: Product catalog with categories and costs

This data is automatically loaded when you run the setup script.

## 🔍 Verification and Monitoring

### Check Environment Status

```python
from snowflake_lab import SnowflakeConfigSetup

setup = SnowflakeConfigSetup("snowflake_environment.yaml")
if setup.connect():
    # List databases
    databases = setup.db_manager.list_databases()
    print(f"Found {len(databases)} databases")

    # List schemas
    schemas = setup.db_manager.list_schemas("PYTHON_LEARNING_LAB")
    print(f"Found {len(schemas)} schemas in PYTHON_LEARNING_LAB")
```

### Run Analytics Queries

The configuration includes pre-built analytics queries that demonstrate:

- Employee summary by department
- Sales performance analysis
- Product profitability calculations
- Employee status analysis

## 🚨 Troubleshooting

### Common Issues

1. **Connection Failed**
   - Check your `.env` file has correct credentials
   - Verify your private key path is correct
   - Ensure your Snowflake account is accessible

2. **Permission Denied**
   - Make sure your user has the necessary roles
   - Check that your role has proper permissions
   - Verify database and schema creation permissions

3. **Configuration Not Found**
   - Ensure the configuration file path is correct
   - Check that the YAML syntax is valid
   - Verify all required fields are present

### Debug Mode

Enable debug logging to see detailed information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔄 Environment Management

### Reset Environment

To reset your environment:

```python
# Drop and recreate all objects
setup = SnowflakeConfigSetup("snowflake_environment.yaml")
if setup.connect():
    # Drop tables
    setup.session.sql("DROP TABLE IF EXISTS PYTHON_LEARNING_LAB.EXAMPLES.EMPLOYEES")
    setup.session.sql("DROP TABLE IF EXISTS PYTHON_LEARNING_LAB.EXAMPLES.SALES_DATA")
    setup.session.sql("DROP TABLE IF EXISTS PYTHON_LEARNING_LAB.EXAMPLES.PRODUCTS")

    # Recreate environment
    setup.setup_environment()
```

### Update Configuration

To update your configuration:

1. Edit the YAML file
2. Run the setup script again
3. The system will use `IF NOT EXISTS` clauses to avoid conflicts

## 🚀 Pydantic V2 Migration

This configuration system has been fully migrated to **Pydantic V2** for enhanced performance and validation:

### **Key Configuration Changes:**

1. **Field Name Updates:**
   - `schema` → `schema_name` (to avoid shadowing Pydantic's built-in `schema` method)
   - All configuration files updated accordingly

2. **Enhanced Environment Variable Resolution:**
   - Automatic `.env` file loading
   - Support for `${VARIABLE}` substitution in YAML files
   - Improved error handling and validation

3. **Updated Validation:**
   - Uses `@field_validator` instead of `@validator`
   - Enhanced type checking and error messages
   - Better performance with Pydantic V2

### **Migration Benefits:**

- ✅ **Better Performance**: Pydantic V2 is significantly faster
- ✅ **Enhanced Validation**: More robust type checking
- ✅ **Cleaner Code**: No deprecation warnings
- ✅ **Future-Proof**: Uses latest Pydantic features

## 🎯 Best Practices

1. **Use Environment Variables**: Store sensitive information in `.env` files
2. **Version Control**: Keep configuration files in version control (but not `.env`)
3. **Environment Separation**: Use different config files for different environments
4. **Documentation**: Document your configuration choices
5. **Testing**: Test your configuration in a development environment first
6. **Pydantic V2**: Use the updated field names and validation patterns

## 🔗 Integration with AI Agents

The configuration system is designed to work seamlessly with lab_0004 AI agents:

```python
# AI agent can read configuration
config = ConfigManager.load_from_file("snowflake_environment.yaml")
database = config.get("environment.database.name")
schema = config.get("environment.schema.name")

# AI agent can generate queries using configured objects
query = f"SELECT * FROM {database}.{schema}.EMPLOYEES WHERE department = 'Engineering'"
```

This makes it easy to build AI-powered data analytics tools that understand your Snowflake environment structure.

## 📚 Next Steps

1. **Customize Configuration**: Modify `snowflake_environment.yaml` for your needs
2. **Add More Tables**: Define additional tables in the configuration
3. **Create More Roles**: Add role-based access control
4. **Build Analytics**: Use the sample data to build analytics dashboards
5. **Integrate with AI**: Connect with lab_0004 AI agents for intelligent data analysis

Your Snowflake environment is now fully configured and ready for development! 🎉
