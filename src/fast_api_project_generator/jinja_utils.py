"""This module contains utility functions for Jinja templates."""

# Define the mapping from SQLAlchemy to Pydantic types
SQLALCHEMY_TO_PYDANTIC_TYPE_MAP = {
    "Integer": "int",
    "String": "str",
    "Text": "str",
    "Boolean": "bool",
    "Date": "date",
    "DateTime": "datetime",
    "Float": "float",
    "Numeric": "float",
    "Time": "time",
    "LargeBinary": "bytes",
}


def pluralize(name: str) -> str:
    """Pluralize a name."""
    if name.endswith("s"):
        return name
    return name + "s"


def collect_sqlalchemy_types(config):
    """Collect the SQLAlchemy types used in the configuration."""
    sqlalchemy_type_set = set()

    for table in config["tables"]:
        for column in table["columns"]:
            sqlalchemy_type_set.add(column["type"])

    return sorted(sqlalchemy_type_set)  # Sort to keep imports ordered
