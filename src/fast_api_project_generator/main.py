"""This module contains the main CLI application for the FastAPI project generator."""

import json
import os
import shutil
from pathlib import Path

import typer
from jinja2 import Environment, FileSystemLoader

from .jinja_utils import (
    SQLALCHEMY_TO_PYDANTIC_TYPE_MAP,
    collect_sqlalchemy_types,
    pluralize,
)
from .utils import (
    get_file_info,
    get_output_filename,
    get_output_path,
    render_template,
    run_command,
    update_pyproject_toml,
)

app = typer.Typer()


@app.command()
def generate(
    output_dir: Path = typer.Option(
        Path("."), help="The directory to output the generated project"
    ),
    config_file: Path = typer.Option(
        "config.json", help="Path to the configuration file"
    ),
):
    """Generate a new FastAPI project."""
    # Load configuration from JSON file
    if not config_file.exists():
        typer.echo(f"Configuration file not found: {config_file}")
        raise FileNotFoundError(f"Configuration file not found: {config_file}")

    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)

    sqlalchemy_types = collect_sqlalchemy_types(config)

    # Set up Jinja2 environment
    env = Environment(
        loader=FileSystemLoader("./src/fast_api_project_generator/templates")
    )
    env.globals["pluralize"] = pluralize
    env.globals["type_map"] = SQLALCHEMY_TO_PYDANTIC_TYPE_MAP

    # Define project-specific variables
    project_name = config["project_name"]
    project_snake_case = project_name.lower().replace(" ", "_")
    project_path = Path(output_dir) / project_snake_case

    # Add project-specific variables to the configuration
    config["project_snake_case"] = project_snake_case

    # Delete the output directory if it exists
    if project_path.exists():
        typer.echo(f"Deleting existing project directory: {project_path}")
        shutil.rmtree(project_path)

    # Create a new Poetry project
    run_command(f"poetry new --src {project_path}")

    # Update `pyproject.toml` with project metadata
    update_pyproject_toml(
        project_path, config["author_name"], config["description"], config["version"]
    )

    # Define templates to render with their input/output paths
    templates = get_file_info("./src/fast_api_project_generator/templates")

    # Render all defined templates
    for template in templates:
        output_file_path = get_output_path(template, project_path, project_snake_case)
        outfile_name = get_output_filename(template, output_file_path, project_path)

        # Create the output directory if it doesn't exist
        os.makedirs(output_file_path, exist_ok=True)

        render_template(
            template["dir"] + "/" + template["filename"] + ".j2",
            {"config": config, "sqlalchemy_types": sqlalchemy_types},
            env,
            outfile_name,
        )

    # Install dependencies using Poetry
    typer.echo(f"Installing dependencies in '{project_path}'...")

    # Add additional libraries
    libraries = "fastapi,uvicorn,sqlalchemy,pydantic_settings,psycopg2-binary,httpx"
    for lib in libraries.split(","):
        run_command(f"poetry add {lib.strip()}", cwd=project_path)

    # Add dev dependencies
    dev_libraries = "pytest,pytest-cov,docker,faker"
    for lib in dev_libraries.split(","):
        run_command(f"poetry add {lib.strip()} --dev", cwd=project_path)

    typer.echo(
        f"Project '{project_name}' generated and dependencies installed in '{project_path}'"
    )

    # Open the project in VSCode
    typer.echo("Opening the project in VSCode...")
    run_command(f"code {project_path}")


if __name__ == "__main__":
    app()
