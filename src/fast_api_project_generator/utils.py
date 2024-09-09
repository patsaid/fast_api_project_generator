"""Helper functions for the `fastapi-project-generator` project."""

import subprocess
from pathlib import Path

import toml
import typer
from jinja2 import Environment


def run_command(command: str, cwd: Path = None):
    """Run a shell command and handle errors."""
    result = subprocess.run(
        command, shell=True, cwd=cwd, text=True, capture_output=True, check=True
    )
    if result.returncode != 0:
        typer.echo(f"Error running command: {command}")
        typer.echo(result.stderr)
        raise RuntimeError(result.stderr)
    return result.stdout


def update_pyproject_toml(project_path, author_name, description, version):
    """Update the metadata in the `pyproject.toml` file."""
    pyproject_file = f"{project_path}/pyproject.toml"

    # Load existing pyproject.toml
    pyproject_data = toml.load(pyproject_file)

    # Update the metadata
    pyproject_data["tool"]["poetry"]["authors"] = [author_name]
    pyproject_data["tool"]["poetry"]["description"] = description
    pyproject_data["tool"]["poetry"]["version"] = version

    # Save the updated pyproject.toml
    with open(pyproject_file, "w", encoding="utf-8") as f:
        toml.dump(pyproject_data, f)


def render_template(
    template_name: str, context: dict, env: Environment, output_path: Path
):
    """Render a template and write it to a file."""
    template = env.get_template(template_name)
    rendered_content = template.render(context)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered_content)


def get_file_info(folder_path):
    """Get information about all files in a folder."""
    folder = Path(folder_path)
    file_info_list = []
    for file in folder.rglob("*"):
        if file.is_file():
            file_info = {
                "dir": str(file.parent.relative_to(folder)),
                "filename": file.stem,
            }
            file_info_list.append(file_info)
    return file_info_list


def get_output_path(template, project_path, project_snake_case):
    """Determine the output file path for a template."""
    output_file_path = project_path / Path(template["dir"])

    # Special case for src directory
    if template["dir"] == "src":
        output_file_path = project_path / "src" / project_snake_case
    # Special case .vscode directory
    elif template["dir"] == ".vscode":
        output_file_path = project_path / ".vscode"

    return output_file_path


def get_output_filename(template, output_file_path, project_path):
    """Determine the output file name for a template."""
    outfile_name = output_file_path / (template["filename"] + ".py")
    # Special case for .env file
    if template["filename"] == ".env":
        outfile_name = output_file_path / ".env"
    # Special case for Dockerfile
    elif template["filename"] == "Dockerfile":
        outfile_name = project_path / template["filename"]
    # Special case for docker-compose.yml
    elif template["filename"] == "docker-compose":
        outfile_name = project_path / "docker-compose.yml"
    # Special case for .gitignore file
    elif template["filename"] == ".gitignore":
        outfile_name = project_path / ".gitignore"
    # Special case for README file
    elif template["filename"] == "README":
        outfile_name = project_path / "README.md"
    # Special case for .vscode/settings.json file
    elif template["filename"] == "settings":
        outfile_name = project_path / ".vscode/settings.json"

    return outfile_name
