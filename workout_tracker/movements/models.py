from django.db import models
from core.models import OwnedMultiAliasResource


class Movement(OwnedMultiAliasResource):
    equipment = models.ForeignKey('equipment.Equipment', related_name='movements', on_delete=models.CASCADE)
    muscles = models.ManyToManyField('muscles.MuscleGrouping', related_name='movements')
    description = models.TextField()
