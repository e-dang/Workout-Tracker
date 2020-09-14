from core.filters import OwnedMultiAliasResourceFilterSet
from .models import ExerciseTemplate


class ExerciseTemplateFilterSet(OwnedMultiAliasResourceFilterSet):
    class Meta:
        model = ExerciseTemplate
        fields = ['workloads__movement']
