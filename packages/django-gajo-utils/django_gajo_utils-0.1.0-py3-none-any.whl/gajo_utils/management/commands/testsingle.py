import importlib
from pathlib import Path

from django.apps import AppConfig, apps
from django.core.management import BaseCommand, call_command
from django.core.management.base import CommandParser
from django.test import TestCase


class Command(BaseCommand):
    help = (
        "With this command you can test only one test_func or TestClass at a time"
        "without specifying full path to test."
    )

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("name", nargs="+", type=str)

    def handle(self, *args, **options) -> None:
        test_name = options["name"][0]

        commands = []

        app: AppConfig
        for app in apps.get_app_configs():
            if app.name.startswith("django"):
                continue

            app_path = Path(app.path)
            test_dir_path: Path = app_path.joinpath("tests")
            test_file_path: Path = app_path.joinpath("tests.py")

            modules = []
            if test_dir_path.exists():
                for file in test_dir_path.iterdir():
                    if not file.stem.startswith("test_"):
                        continue
                    module_path = f"{app.name}.tests.{file.stem}"
                    modules.append(importlib.import_module(module_path))
            if test_file_path.exists():
                module_path = f"{app.name}.{test_file_path.stem}"
                modules.append(importlib.import_module(module_path))

            for module in modules:
                if hasattr(module, test_name):
                    command = f"{module.__name__}.{test_name}"
                    commands.append(command)

                for k, v in module.__dict__.items():
                    if isinstance(v, type) and issubclass(v, TestCase):
                        if hasattr(v, test_name):
                            command = f"{module.__name__}.{k}.{test_name}"
                            commands.append(command)

        if len(commands) == 0:
            print("No test_func or TestClass found by provided name(s).")
            return

        for command in commands:
            print(f"Testing: {command}")
            call_command("test", command)
