from django.db import models
from core.models import OwnedMultiAliasResource


class Movement(OwnedMultiAliasResource):
    equipment = models.ManyToManyField('equipment.Equipment', related_name='movements')
    muscles = models.ManyToManyField('muscles.MuscleGrouping', related_name='movements')
    description = models.TextField()
