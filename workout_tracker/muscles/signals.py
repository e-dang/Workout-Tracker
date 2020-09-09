from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from .models import MuscleSubportion, Muscle, MuscleGrouping
from .utils import percolate, enforce_no_empty_relationships


@receiver(pre_delete, sender=MuscleSubportion)
def enforce_no_empty_relationships_on_muscles(sender, instance, **kwargs):
    enforce_no_empty_relationships(instance, 'muscles', 'subportions')


@receiver(pre_delete, sender=Muscle)
def enforce_no_empty_relationships_on_muscle_groupings(sender, instance, **kwargs):
    enforce_no_empty_relationships(instance, 'groupings', 'muscles')


@receiver(post_save, sender=MuscleSubportion)
def percolate_to_muscle(sender, instance, created, **kwargs):
    percolate(instance, created, Muscle, 'subportions')


@receiver(post_save, sender=Muscle)
def percolate_to_muscle_grouping(sender, instance, created, **kwargs):
    percolate(instance, created, MuscleGrouping, 'muscles')
