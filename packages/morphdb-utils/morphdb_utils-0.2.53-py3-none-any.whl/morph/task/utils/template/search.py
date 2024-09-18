import json
from pathlib import Path
from typing import Optional

import click
import pydantic

from morph.cli.flags import Flags
from morph.task.base import BaseTask
from morph.task.utils.morph import find_project_root_dir
from morph.task.utils.template.inspection import (
    MorphRegistryTemplateItem,
    MorphRegistryTemplateResponse,
)
from morph.task.utils.template.state import load_cache


class SearchTemplateTask(BaseTask):
    def __init__(self, args: Flags):
        super().__init__(args)
        self.args = args

    def run(self):
        try:
            project_root = find_project_root_dir()
        except FileNotFoundError as e:
            click.echo(click.style(str(e), fg="red"))
            raise e

        name: Optional[str] = self.args.NAME
        language: Optional[str] = self.args.LANGUAGE
        query: Optional[str] = self.args.QUERY
        limit: int = self.args.LIMIT
        skip: int = self.args.SKIP

        # Load user defined templates from cache
        try:
            cache = load_cache(project_root)
        except (pydantic.ValidationError, json.decoder.JSONDecodeError):
            click.echo(
                click.style(
                    "Warning: Morph-cli template cache is corrupted. Please recompile the templates.",
                    fg="yellow",
                )
            )
            return

        if not cache:
            click.echo(
                click.style(
                    "Warning: No template cache found in the project. Please compile the templates first.",
                    fg="yellow",
                )
            )
            result = MorphRegistryTemplateResponse(templates=[], count=0)
            click.echo(result.model_dump_json(indent=2))
            return

        # Filter the templates based on the search criteria
        filtered_templates = []
        for item in cache.items:
            if name and item.spec.name != name:
                continue
            if language and item.spec.language != language:
                continue
            if query and not (
                query in item.spec.name
                or (item.spec.description and query in item.spec.description)
            ):
                continue

            path = Path(item.file_path)
            src_path = path if path.is_absolute() else project_root / path

            filtered_templates.append(
                MorphRegistryTemplateItem(
                    name=item.spec.name,
                    title=item.spec.title,
                    description=item.spec.description,
                    code=src_path.read_text(),
                    language=item.spec.language,
                )
            )

        # Paginate the filtered templates
        total_count = len(filtered_templates)
        paginated_templates = filtered_templates[skip : skip + limit]

        result = MorphRegistryTemplateResponse(
            templates=paginated_templates,
            count=total_count,
        )
        click.echo(result.model_dump_json(indent=2))
