from pydantic import BaseModel, Field
from typing import List, Optional

from sungen.utils.yaml_tools import YAMLMixin
import os
import subprocess
import typer
import yaml

app = typer.Typer(
    name="blueprint",
    help="Plugin for creating, managing, and executing blueprints in Aider."
)

class AiderBlueprint(BaseModel, YAMLMixin):
    """Defines a Blueprint for using Aider."""
    module_name: str = Field(..., description="Name of the blueprint module.")
    version: str = Field(default="1.0.0", description="Version of the blueprint.")
    description: str = Field(..., description="Description of the blueprint.")
    files_to_create: List[str] = Field(..., description="List of files to be created.")
    files_to_edit: List[str] = Field(..., description="List of files to be edited.")
    read_only_files: List[str] = Field(default_factory=list, description="List of files to be marked as read-only.")
    model: str = Field(default="gpt-4", description="AI model to use.")
    auto_test: bool = Field(default=True, description="Enable or disable automatic testing after edits.")
    lint: bool = Field(default=True, description="Enable or disable linting of files.")
    pretty_output: bool = Field(default=True, description="Enable or disable colorized output.")
    dark_mode: bool = Field(default=False, description="Set terminal output theme to dark mode.")
    additional_args: Optional[List[str]] = Field(default_factory=list, description="Additional command-line arguments for Aider.")
    message: str = Field(None, description="Custom message to use for the Aider command.")
    context_files: List[str] = Field(default_factory=list, description="List of relevant context files.")
    conventions_file: str = Field(default="CONVENTIONS.md", description="File containing coding conventions.")


def create_blueprint_logic(blueprint_name: str, description: str, files_to_create: List[str], files_to_edit: List[str],
                           read_only_files: List[str], model: str, auto_test: bool, lint: bool,
                           pretty_output: bool, dark_mode: bool, additional_args: List[str], message: str):
    """
    Logic for creating a new blueprint.
    """
    blueprint = AiderBlueprint(
        module_name=blueprint_name,
        description=description,
        files_to_create=files_to_create,
        files_to_edit=files_to_edit,
        read_only_files=read_only_files,
        model=model,
        auto_test=auto_test,
        lint=lint,
        pretty_output=pretty_output,
        dark_mode=dark_mode,
        additional_args=additional_args,
        message=message
    )

    blueprint_file = f"{blueprint_name}.yml"
    blueprint.to_yaml(blueprint_file)
    typer.echo(f"Blueprint '{blueprint_name}' created and saved to {blueprint_file}.")


def list_blueprints_logic():
    """Logic for listing all available blueprints."""
    blueprints = [f for f in os.listdir() if f.endswith(".yml")]
    if not blueprints:
        typer.echo("No blueprints found.")
    else:
        typer.echo("Available blueprints:")
        for blueprint in blueprints:
            typer.echo(f"- {blueprint}")


def run_blueprint_logic(blueprint_file: str):
    """Logic for running a specified blueprint."""
    # Load the blueprint from the YAML file
    with open(blueprint_file, "r") as file:
        blueprint_data = yaml.safe_load(file)

    blueprint = AiderBlueprint(**blueprint_data)

    # Step 1: Handle `files_to_create` - Create any files that are listed
    for file_to_create in blueprint.files_to_create:
        if not os.path.exists(file_to_create):
            typer.echo(f"Creating file: {file_to_create}")
            with open(file_to_create, 'w') as f:
                # Add default content, like a "Hello World" script for Python files
                if file_to_create.endswith('.py'):
                    f.write('print("Hello, World!")\n')
                else:
                    f.write('')  # Create an empty file for other types

    # Step 2: Construct the base aider command
    command = [
        "aider",
        "--file", ",".join(blueprint.files_to_edit),  # Edit specified files
        "--model", blueprint.model,  # Use the specified AI model
        "--yes"  # Assume yes to all prompts for smoother automation
    ]

    # Step 3: Handle `read_only_files` - Add read-only files to the command
    for read_only_file in blueprint.read_only_files:
        command.extend(["--read", read_only_file])  # Specify files as read-only

    # Step 4: Handle boolean options (`auto_test`, `lint`, `pretty_output`, `dark_mode`)
    if blueprint.auto_test:
        command.append("--auto-test")
    if blueprint.lint:
        command.append("--lint")
    if blueprint.pretty_output:
        command.append("--pretty")
    if blueprint.dark_mode:
        command.append("--dark-mode")

    # Step 5: Add `conventions_file` to the files to be edited
    if blueprint.conventions_file:
        command.extend(["--read", blueprint.conventions_file])

    # Step 6: Handle `context_files` - Add any context files as read-only files
    for context_file in blueprint.context_files:
        command.extend(["--read", context_file])

    # Step 7: Handle `additional_args` - Append any extra arguments
    command.extend(blueprint.additional_args)

    # Step 8: Handle `message` - Add the custom message option if provided
    if blueprint.message:
        command.append(f"--message={blueprint.message}")

    # Print and execute the command
    typer.echo(f"Running command: {' '.join(command)}")
    subprocess.run(command)



def delete_blueprint_logic(blueprint_file: str):
    """Logic for deleting an existing blueprint."""
    if os.path.exists(blueprint_file):
        os.remove(blueprint_file)
        typer.echo(f"Blueprint {blueprint_file} deleted.")
    else:
        typer.echo(f"Blueprint {blueprint_file} does not exist.")


@app.command()
def create_blueprint(
        blueprint_name: str = typer.Argument(..., help="Name of the new blueprint"),
        description: str = typer.Option(..., help="Description of the blueprint"),
        files_to_create: List[str] = typer.Option([], help="List of files to be created"),
        files_to_edit: List[str] = typer.Option([], help="List of files to be edited"),
        read_only_files: List[str] = typer.Option([], help="List of read-only files"),
        model: str = typer.Option("gpt-4", help="AI model to use"),
        auto_test: bool = typer.Option(True, help="Enable or disable automatic testing"),
        lint: bool = typer.Option(True, help="Enable or disable linting"),
        pretty_output: bool = typer.Option(True, help="Enable or disable pretty output"),
        dark_mode: bool = typer.Option(False, help="Enable or disable dark mode"),
        additional_args: List[str] = typer.Option([], help="Additional arguments for Aider"),
        message: str = typer.Option("", help="Custom message to use for Aider")
):
    """
    Create a new blueprint.
    """
    create_blueprint_logic(
        blueprint_name, description, files_to_create, files_to_edit, read_only_files,
        model, auto_test, lint, pretty_output, dark_mode, additional_args, message
    )


@app.command()
def list_blueprints():
    """List all available blueprints."""
    list_blueprints_logic()


@app.command()
def run_blueprint(blueprint_file: str):
    """Run a specified blueprint."""
    run_blueprint_logic(blueprint_file)


@app.command()
def delete_blueprint(blueprint_file: str):
    """Delete an existing blueprint."""
    delete_blueprint_logic(blueprint_file)


def main():
    # Define the blueprint parameters
    blueprint_name = "hello_world_blueprint"
    description = "A blueprint to create a Hello World Python script."
    files_to_create = ["hello_world.py"]
    files_to_edit = ["hello_world.py"]
    read_only_files = ["Users/sac/dev/sungen/src/sungen/plugins/blueprint/.context.md"]
    model = "gpt-4o-mini"
    auto_test = False
    lint = False
    pretty_output = True
    dark_mode = False
    additional_args = []
    message = "Creating a Hello World Python file using Aider."

    # Create the blueprint
    # create_blueprint_logic(
    #     blueprint_name=blueprint_name,
    #     description=description,
    #     files_to_create=files_to_create,
    #     files_to_edit=files_to_edit,
    #     read_only_files=read_only_files,
    #     model=model,
    #     auto_test=auto_test,
    #     lint=lint,
    #     pretty_output=pretty_output,
    #     dark_mode=dark_mode,
    #     additional_args=additional_args,
    #     message=message
    # )

    # Run the blueprint
    run_blueprint_logic(f"{blueprint_name}.yml")


if __name__ == "__main__":
    # app()  # Existing Typer CLI app entry point
    main()

