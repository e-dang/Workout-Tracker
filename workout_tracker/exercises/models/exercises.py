from core.models import OwnedMultiAliasResource
from django.db import models
from .workloads import WorkloadTemplate, Workload, WorkloadTemplateProxy, WorkloadProxy
from exercises.managers import ExerciseTemplateManager


class AbstractExercise(OwnedMultiAliasResource):
    class Meta:
        abstract = True

    def __repr__(self):
        return '\n'.join([str(self)] + [str(workload) for workload in self.workloads.all()])

    def __getitem__(self, idx):
        return self._create_proxy(self._get(idx))

    def __delitem__(self, idx):
        workload = self._get(idx)

        # fix ordering of workloads such that they all are adjacent to each other
        self.workloads.filter(order__gt=workload.order).update(order=models.F('order') - 1)
        workload.delete()

    def __len__(self):
        return self.workloads.all().count()

    def append(self, movement, units, order=None, sets=None):
        workload = self.workloads.create(movement=movement, units=units, order=order or len(self))
        if sets is not None:
            for _set in sets:
                workload.append(**_set)

    def extend(self, workloads):
        for workload in workloads:
            self.append(**workload)

    def remove(self, idx):
        del self[idx]

    def _get(self, idx):
        try:
            return self.workloads.get(order=idx)
        except (WorkloadTemplate.DoesNotExist, Workload.DoesNotExist):
            raise KeyError('Index out of range.')

    def _create_proxy(self, workload):
        raise NotImplementedError


class ExerciseTemplate(AbstractExercise):

    objects = ExerciseTemplateManager()

    def create_exercise(self):
        return Exercise.from_template(self)

    def _create_proxy(self, workload):
        return WorkloadTemplateProxy(workload)


class Exercise(AbstractExercise):

    @classmethod
    def from_template(cls, template):
        exercise = cls.objects.create(owner=template.owner, name=template.name, snames=template.snames)
        for workload_template in template.workloads.all():
            workload_template.create_workload(exercise)
        return exercise

    @property
    def is_complete(self):
        return all([workload.is_complete for workload in self.workloads.all()])

    def _create_proxy(self, workload):
        return WorkloadProxy(workload)
