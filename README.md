# FastAPI Project Generator

A tool for generating a FastAPI project structure with customizable templates.

## Features

- Generate a new FastAPI project with a predefined structure.
- Customizable templates for code generation.
- CLI interface for easy use.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/patsaid/fast_api_project_generator.git
   cd fast-api-project-generator
   ```

2. **Install Dependencies**

    ```bash
   poetry install
   ```

## Usage
To generate a new FastAPI project, use the following command:

```bash
poetry run generate-project --output-dir <path_to_output> --config-file ./config.json
```

- <path_to_output>: The directory where the project should be generated.

### Configuration File

This project uses a configuration file to define various settings. The configuration file is in JSON format and allows you to specify database tables, relationships, and other settings for the project.

#### Configuration File Format

The configuration file should be named config.json and placed in the root of your project directory. Below is an example format:

```json
{
  "project_name": "FastAPI Generated Project",
  "author_name": "John Doe",
  "description": "This is a FastAPI generated project.",
  "version": "0.1.0",
  "postgresql": {
    "user": "postgres",
    "password": "postgres"
  },
  "tables": [
    {
      "name": "user",
      "columns": [
        {
          "name": "id",
          "type": "Integer",
          "primary_key": true,
          "auto_increment": true
        },
        {
          "name": "name",
          "type": "String",
          "nullable": false,
          "max_length": 100,
          "default": "''"
        },
        {
          "name": "email",
          "type": "String",
          "nullable": false,
          "unique": true,
          "index": true
        }
      ],
      "relationships": [
        {
          "name": "posts",
          "related_table": "post",
          "back_populates": "user"
        }
      ],
      "methods": ["GET", "POST", "PUT", "DELETE"]
    },
    {
      "name": "post",
      "columns": [
        {
          "name": "id",
          "type": "Integer",
          "primary_key": true,
          "auto_increment": true
        },
        {
          "name": "title",
          "type": "String",
          "nullable": false,
          "max_length": 100
        },
        {
          "name": "content",
          "type": "Text",
          "nullable": false
        },
        {
          "name": "user_id",
          "type": "Integer",
          "foreign_key": {
            "table": "user",
            "column": "id"
          }
        }
      ],
      "relationships": [
        {
          "name": "user",
          "related_table": "user",
          "back_populates": "posts"
        }
      ],
      "methods": ["GET", "POST", "PUT", "DELETE"]
    }
  ]
}
```

#### Description of Fields

- project_name: The name of the project.
- database.url: The connection URL for the database.
- tables: A list of tables with their respective columns and types.
- name: The name of the table.
- columns: A list of columns in the table.
- name: The name of the column.
type: The SQLAlchemy type of the column (e.g., Integer, String).
- primary_key: Whether the column is a primary key.
- nullable: Whether the column allows NULL values.
- foreign_key: The column this one is a foreign key for (optional).
- relationships: A list of relationships between tables.
- source: The source table.
- target: The target table.
- type: The type of relationship (e.g., one_to_many).
- source_column: The column in the source table.
- target_column: The column in the target table.

This configuration allows you to define your database schema and relationships in a structured format, which can then be used to generate your FastAPI project.

### Example

```bash
poetry run generate-project --config_file config.json --output-dir ~/Desktop/fastapi_gen
```

This command will create a new FastAPI project in the ~/Desktop/fastapi_gen directory.


## License
This project is licensed under the MIT License - see the LICENSE file for details.