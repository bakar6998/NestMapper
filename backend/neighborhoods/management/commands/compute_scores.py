from django.core.management.base import BaseCommand
from neighborhoods.scoring import compute_all_scores


class Command(BaseCommand):
    """
    Django management command to compute
    scores for all neighborhoods.

    Run with:
    python manage.py compute_scores
    """
    help = 'Compute scores for all neighborhoods'

    def handle(self, *args, **kwargs):
        self.stdout.write(
            self.style.SUCCESS(
                'Starting score computation...'
            )
        )

        try:
            compute_all_scores()
            self.stdout.write(
                self.style.SUCCESS(
                    'All scores computed successfully!'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Error computing scores: {e}'
                )
            )