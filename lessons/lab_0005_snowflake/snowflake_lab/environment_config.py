"""
Extended configuration models for Snowflake environment setup.

This module defines Pydantic models for database, schema, warehouse,
and other Snowflake object configurations.
"""

from typing import Any

from pydantic import BaseModel, Field


class DatabaseConfig(BaseModel):
    """Configuration for Snowflake database creation."""

    name: str = Field(..., description="Database name")
    if_not_exists: bool = Field(True, description="Use IF NOT EXISTS clause")
    comment: str | None = Field(None, description="Database comment")
    data_retention_time_in_days: int | None = Field(
        None, description="Data retention period in days"
    )
    owner: str | None = Field(None, description="Database owner role")


class SchemaConfig(BaseModel):
    """Configuration for Snowflake schema creation."""

    schema_name: str = Field(..., description="Schema name")
    database: str | None = Field(None, description="Parent database name")
    if_not_exists: bool = Field(True, description="Use IF NOT EXISTS clause")
    comment: str | None = Field(None, description="Schema comment")
    managed_access: bool = Field(False, description="Enable managed access")
    owner: str | None = Field(None, description="Schema owner role")


class WarehouseConfig(BaseModel):
    """Configuration for Snowflake warehouse creation."""

    name: str = Field(..., description="Warehouse name")
    if_not_exists: bool = Field(True, description="Use IF NOT EXISTS clause")
    size: str = Field("X-SMALL", description="Warehouse size")
    auto_suspend: int = Field(60, description="Auto-suspend time in seconds")
    auto_resume: bool = Field(True, description="Auto-resume enabled")
    comment: str | None = Field(None, description="Warehouse comment")
    owner: str | None = Field(None, description="Warehouse owner role")
    min_cluster_count: int = Field(1, description="Minimum cluster count")
    max_cluster_count: int = Field(1, description="Maximum cluster count")


class RoleConfig(BaseModel):
    """Configuration for Snowflake role creation."""

    name: str = Field(..., description="Role name")
    if_not_exists: bool = Field(True, description="Use IF NOT EXISTS clause")
    comment: str | None = Field(None, description="Role comment")
    owner: str | None = Field(None, description="Role owner")


class UserConfig(BaseModel):
    """Configuration for Snowflake user creation."""

    name: str = Field(..., description="User name")
    if_not_exists: bool = Field(True, description="Use IF NOT EXISTS clause")
    display_name: str | None = Field(None, description="User display name")
    email: str | None = Field(None, description="User email")
    default_role: str | None = Field(None, description="Default role")
    default_warehouse: str | None = Field(
        None, description="Default warehouse"
    )
    default_namespace: str | None = Field(
        None, description="Default namespace"
    )
    rsa_public_key: str | None = Field(
        None, description="RSA public key for key-pair auth"
    )
    comment: str | None = Field(None, description="User comment")
    must_change_password: bool = Field(
        False, description="Must change password on first login"
    )


class TableConfig(BaseModel):
    """Configuration for Snowflake table creation."""

    name: str = Field(..., description="Table name")
    schema_name: str | None = Field(None, description="Parent schema name")
    database: str | None = Field(None, description="Parent database name")
    if_not_exists: bool = Field(True, description="Use IF NOT EXISTS clause")
    columns: list[dict[str, Any]] = Field(
        ..., description="Column definitions"
    )
    comment: str | None = Field(None, description="Table comment")
    owner: str | None = Field(None, description="Table owner role")


class EnvironmentConfig(BaseModel):
    """Complete environment configuration for Snowflake setup."""

    database: DatabaseConfig | None = Field(
        None, description="Database configuration"
    )
    schema_config: SchemaConfig | None = Field(
        None, description="Schema configuration"
    )
    warehouse: WarehouseConfig | None = Field(
        None, description="Warehouse configuration"
    )
    roles: list[RoleConfig] = Field(
        default_factory=list, description="Roles to create"
    )
    users: list[UserConfig] = Field(
        default_factory=list, description="Users to create"
    )
    tables: list[TableConfig] = Field(
        default_factory=list, description="Tables to create"
    )
    grants: list[dict[str, Any]] = Field(
        default_factory=list, description="Grants to execute"
    )


class SnowflakeEnvironmentConfig(BaseModel):
    """Extended Snowflake configuration including environment setup."""

    connection: Any = Field(
        ..., description="Connection settings (from existing config)"
    )
    environment: EnvironmentConfig | None = Field(
        None, description="Environment setup configuration"
    )
    project: dict[str, Any] | None = Field(
        None, description="Project-specific settings"
    )
