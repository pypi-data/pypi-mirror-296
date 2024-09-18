import os.path

from django.apps import apps

from django.core.management import BaseCommand, call_command
from gajo_utils import get_config


class Command(BaseCommand):
    help = "Load fixtures from and in order that is specified in LOAD_FIXTURES config."

    def handle(self, *args, **options) -> None:
        LOAD_FIXTURES = get_config().get("LOAD_FIXTURES")

        # First check if all models exists (raises LookupError)
        for model in LOAD_FIXTURES:
            apps.get_model(model)

        # First we check if all fixture files that are referencing models exists
        if not os.path.isdir("fixtures"):
            raise LookupError('"fixtures" directory doesn\'t exists.')

        for model in LOAD_FIXTURES:
            app_name, model_name = model.split(".")

            if not os.path.isdir(f"fixtures/{app_name}"):
                raise LookupError(f'"/fixtures/{app_name}" directory doesn\'t exists.')

            if not os.path.isfile(f"fixtures/{app_name}/{model_name}.json"):
                raise LookupError(
                    f'"fixtures/{app_name}/{model_name}.json" file doesn\'t exists.'
                )

        # After all checks we can load fixtures
        for model in LOAD_FIXTURES:
            app_name, model_name = model.split(".")
            call_command("loaddata", f"fixtures/{app_name}/{model_name}.json")
