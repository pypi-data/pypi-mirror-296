import os

from django.core.management import call_command
from django.core.management.base import BaseCommand

from gajo_utils import get_config
from django.apps import apps


class Command(BaseCommand):
    help = (
        'Dump fixtures from models specified in "DUMP_FIXTURES" in '
        "/fixtures/app/model_name.json structure."
    )

    def handle(self, *args, **options):
        DUMP_FIXTURES = get_config().get("DUMP_FIXTURES")

        # First check if all models exists (raises LookupError)
        for model in DUMP_FIXTURES:
            apps.get_model(model)

        # Create dir and start populating
        if not os.path.isdir("fixtures"):
            os.mkdir("fixtures")

        for model in DUMP_FIXTURES:
            app_name, model_name = model.split(".")
            self._call_dumpdata(app_name, model_name)

    def _call_dumpdata(self, app_name: str, model_name: str):
        if not os.path.isdir(f"fixtures/{app_name}"):
            os.mkdir(f"fixtures/{app_name}")

        call_command(
            "dumpdata",
            f"{app_name}.{model_name}",
            f"--output=fixtures/{app_name}/{model_name}.json",
            "--indent=4",
        )
