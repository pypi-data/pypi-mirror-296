import json
import os
import shutil

import click

from morph.cli.flags import Flags
from morph.config.project import default_initial_project, load_project, save_project
from morph.constants import MorphConstant
from morph.task.base import BaseTask
from morph.task.utils.sqlite import SqliteDBManager

LANG = "en"


class NewTask(BaseTask):
    def __init__(self, args: Flags, project_directory: str):
        super().__init__(args)
        self.args = args
        self.project_directory = project_directory

    def run(self):
        click.echo("Creating new Morph project...")

        # Create the project structure
        if not os.path.exists(self.project_directory):
            os.makedirs(self.project_directory, exist_ok=True)

        db_path = f"{self.project_directory}/morph_project.sqlite3"
        if not os.path.exists(db_path):
            with open(db_path, "w") as f:
                f.write("")

        # Initialize the project database
        db_manager = SqliteDBManager(self.project_directory)
        db_manager.initialize_database()

        # create morph_project.yaml
        project = load_project(self.project_directory)
        if project is not None:
            click.echo(
                f"The directory is already a Morph project: {self.project_directory}"
            )
            return False
        else:
            self._create_project_structure()
            self._save_morph_canvas_json()

        click.echo("Project setup completed successfully.")
        self._display_post_setup_message()
        return True

    def _create_project_structure(self):
        project = default_initial_project()
        save_project(self.project_directory, project)
        directories = [
            ##########################################
            # Sources
            ##########################################
            f"{self.project_directory}/src",
            ##########################################
            # Knowledge
            ##########################################
            f"{self.project_directory}/knowledge",
            ##########################################
            # Canvases
            ##########################################
            f"{self.project_directory}/{MorphConstant.CANVAS_DIR}",
            ##########################################
            # Public/Private
            ##########################################
            f"{self.project_directory}/{MorphConstant.PRIVATE_DIR}",
        ]

        files = {
            ##########################################
            # Canvas
            ##########################################
            f"{self.project_directory}/src/example_python_cell.py": self._generate_example_python_cell(),
            f"{self.project_directory}/src/example_sql_cell.sql": self._generate_example_sql_cell(),
            ##########################################
            # Data
            ##########################################
            f"{self.project_directory}/_private/World_Average_Temperature_2020_2024.csv": self._generate_example_data(),
            ##########################################
            # Knowledge
            ##########################################
            f"{self.project_directory}/knowledge/README.md": self._generate_knowledge_readme(),
            ##########################################
            # Project Root
            ##########################################
            f"{self.project_directory}/morph_project.sqlite3": "",
            f"{self.project_directory}/.env": self._generate_project_dotenv_content(),
            f"{self.project_directory}/.gitignore": self._generate_project_gitignore_content(),
            f"{self.project_directory}/pyproject.toml": self._generate_project_toml_content(),
            f"{self.project_directory}/README.md": self._generate_project_readme(),
        }

        # Create directories
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

        # Create files with default content
        for filepath, content in files.items():
            with open(filepath, "w") as f:
                f.write(content)

        # templatesはディレクトリ構造ごとコピーする
        templates_src = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "template/templates")
        )
        templates_dst = os.path.normpath(
            os.path.join(self.project_directory, "templates")
        )
        os.makedirs(templates_dst, exist_ok=True)
        for t_root, t_dirs, t_files in os.walk(templates_src):
            for t_dir in t_dirs:
                src_dir = os.path.join(t_root, t_dir)
                rel_dir_path = os.path.relpath(src_dir, templates_src)
                dst_dir = os.path.join(templates_dst, rel_dir_path)
                os.makedirs(dst_dir, exist_ok=True)

            for t_file in t_files:
                src = os.path.join(t_root, t_file)
                rel_path = os.path.relpath(src, templates_src)
                dst = os.path.join(templates_dst, rel_path)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)

    def _display_post_setup_message(self):
        message = (
            f"\nTo activate the project environment and install dependencies, "
            f"run the following commands:\n\n"
            f"    cd {os.path.abspath(self.project_directory)}\n"
            f"    poetry install\n\n"
            f"If you don't have Poetry installed, visit https://python-poetry.org/docs/#installation "
            f"for installation instructions.\n"
        )
        click.echo(click.style(message, fg="yellow"))

    @staticmethod
    def _generate_project_readme():
        template_path = os.path.join(
            os.path.dirname(__file__), f"template/{LANG}/README.md"
        )
        with open(template_path, "r") as file:
            return file.read()

    @staticmethod
    def _generate_knowledge_readme():
        template_path = os.path.join(
            os.path.dirname(__file__), f"template/{LANG}/README_knowledge.md"
        )
        with open(template_path, "r") as file:
            return file.read()

    @staticmethod
    def _generate_example_python_cell():
        template_path = os.path.join(
            os.path.dirname(__file__), "template/cells/example_python_cell.py"
        )
        with open(template_path, "r") as file:
            return file.read()

    @staticmethod
    def _generate_example_sql_cell():
        template_path = os.path.join(
            os.path.dirname(__file__), "template/cells/example_sql_cell.sql"
        )
        with open(template_path, "r") as file:
            return file.read()

    @staticmethod
    def _generate_project_dotenv_content():
        dotenv_content = """# Environment Configuration File
# This file contains environment variables that configure the application.
# Each line in this file must be in VAR=VAL format.

# Set the TZ variable to the desired timezone.
# In Morph cloud platform, the change will take effect after the next run.
TZ=Asia/Tokyo"""
        return dotenv_content

    @staticmethod
    def _generate_project_toml_content():
        template_path = os.path.join(
            os.path.dirname(__file__), "template/pyproject.toml"
        )
        with open(template_path, "r") as file:
            return file.read()

    def _save_morph_canvas_json(self):
        canvas_json = {
            "cells": {
                "example_python_cell": {
                    "coordinates": {"x": 0, "y": 0, "w": 600, "h": 400},
                },
                "example_sql_cell": {
                    "coordinates": {"x": 0, "y": 450, "w": 600, "h": 400},
                },
            }
        }
        canvas_json_path = os.path.join(
            self.project_directory, MorphConstant.CANVAS_DIR, "canvas1.canvas.json"
        )
        with open(canvas_json_path, "w") as f:
            f.write(json.dumps(canvas_json, indent=4))

    @staticmethod
    def _generate_project_gitignore_content():
        template_path = os.path.join(os.path.dirname(__file__), "template/.gitignore")
        with open(template_path, "r") as file:
            return file.read()

    @staticmethod
    def _generate_example_data():
        template_path = os.path.join(
            os.path.dirname(__file__),
            "template/data/World_Average_Temperature_2020_2024.csv",
        )
        with open(template_path, "r") as file:
            return file.read()
