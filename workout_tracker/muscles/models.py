from core.models import MultiAliasResource
from django.db import models


class AbstractMuscle(MultiAliasResource):
    name = models.CharField(max_length=100, primary_key=True)
    created = None

    class Meta:
        abstract = True


class MuscleSubportion(AbstractMuscle):
    pass


class Muscle(AbstractMuscle):
    subportions = models.ManyToManyField(MuscleSubportion, related_name='muscles')


class MuscleGrouping(AbstractMuscle):
    muscles = models.ManyToManyField(Muscle, related_name='groupings')
