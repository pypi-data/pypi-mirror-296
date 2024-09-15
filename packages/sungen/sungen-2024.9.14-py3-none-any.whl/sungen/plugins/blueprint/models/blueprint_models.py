from pydantic import BaseModel, Field
from typing import List, Optional

from sungen.utils.yaml_tools import YAMLMixin


class AiderBlueprint(BaseModel, YAMLMixin):
    """Defines a Blueprint for using Aider."""
    module_name: str = Field(..., description="Name of the blueprint module.")
    version: str = Field(default="1.0.0", description="Version of the blueprint.")
    description: str = Field(..., description="Description of the blueprint.")
    files_to_create: List[str] = Field(..., description="List of files to be created.")
    files_to_edit: List[str] = Field(..., description="List of files to be edited.")
    read_only_files: List[str] = Field(default_factory=list, description="List of files to be marked as read-only.")
    model: str = Field(default="gpt-4o-mini", description="AI model to use.")
    auto_test: bool = Field(default=True, description="Enable or disable automatic testing after edits.")
    lint: bool = Field(default=True, description="Enable or disable linting of files.")
    pretty_output: bool = Field(default=True, description="Enable or disable colorized output.")
    dark_mode: bool = Field(default=False, description="Set terminal output theme to dark mode.")
    additional_args: Optional[List[str]] = Field(default_factory=list, description="Additional command-line arguments for Aider.")
    message: str = Field(None, description="Custom message to use for the Aider command.")
    context_files: List[str] = Field(default_factory=list, description="List of relevant context files.")
    conventions_file: str = Field(default="CONVENTIONS.md", description="File containing coding conventions.")
