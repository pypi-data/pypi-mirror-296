from django.core.management.base import BaseCommand
from djing.core.commands.handle_init import handle_init


class Command(BaseCommand):
    help = (
        "Initializes the Djing application. This command sets up necessary configurations and resources "
        "for the Djing application. If the application is already initialized, you can use the --force flag "
        "to reinitialize it and overwrite existing configurations."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help=(
                "Force reinitialization of the Djing application even if it is already initialized. "
                "Use this flag to overwrite existing settings and configurations."
            ),
        )

    def handle(self, *args, **options):
        handle_init(self, *args, **options)
