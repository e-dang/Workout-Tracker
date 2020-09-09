from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from muscles.models import MuscleSubportion, Muscle, MuscleGrouping


class Command(BaseCommand):
    help = '''Deletes all MusclesSubportions, Muscles, and MuscleGroupings from the database then subsequently loads all
    of them back into the database from their respective fixtures.'''

    def handle(self, *args, **options):
        # remove muscles from db
        self._remove_from_db(MuscleSubportion)
        self._remove_from_db(Muscle)
        self._remove_from_db(MuscleGrouping)

        # reload into db
        call_command('loaddata', 'muscle_subportions.json')
        call_command('loaddata', 'muscles.json')
        call_command('loaddata', 'muscle_groupings.json')

        self.stdout.write(self.style.SUCCESS('Successfully imported muscles app data!'))

    def _remove_from_db(self, model):
        model.objects.all().delete()
