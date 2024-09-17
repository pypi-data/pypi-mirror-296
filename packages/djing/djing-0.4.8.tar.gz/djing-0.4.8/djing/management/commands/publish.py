from django.core.management.base import BaseCommand
from djing.core.commands.handle_publish import handle_publish


class Command(BaseCommand):
    help = (
        "published the Djing application. This command sets up necessary configurations and resources "
        "for the Djing application. If the application is already published, you can use the --force flag "
        "to re published it and overwrite existing configurations."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help=(
                "Force re publishing of the Djing application even if it is already published. "
                "Use this flag to overwrite existing settings and configurations."
            ),
        )

    def handle(self, *args, **options):
        handle_publish(self, *args, **options)
