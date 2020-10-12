from django.db import models

from core.models import OwnedMultiAliasResource
from exercises.managers import ExerciseTemplateManager

from .workloads import Workload, WorkloadTemplate


class AbstractExercise(OwnedMultiAliasResource):
    order = models.PositiveSmallIntegerField()

    class Meta:
        abstract = True

    def __repr__(self):
        return '\n'.join([str(self)] + [str(workload) for workload in self.workloads.all()])

    def __getitem__(self, idx):
        if (workload := self.get(idx)) is None:
            raise KeyError('Index out of range.')
        return workload

    def __delitem__(self, idx):
        workload = self[idx]

        # fix ordering of workloads such that they all are adjacent to each other
        self.workloads.filter(order__gt=workload.order).update(order=models.F('order') - 1)
        workload.delete()

    def __len__(self):
        return self.workloads.all().count()

    def get(self, idx, default=None):
        try:
            return self.workloads.get(order=idx)
        except (WorkloadTemplate.DoesNotExist, Workload.DoesNotExist):
            return default

    def append(self, movement, units, order=None, sets=None):
        return self.workloads.create(movement=movement, units=units, order=order or len(self), sets=sets)

    def extend(self, workloads):
        for workload in workloads:
            self.append(**workload)

    def remove(self, idx):
        del self[idx]

    def swap_workloads(self, idx1, idx2):
        workload = self.workloads.get(order=idx1)
        self.workloads.filter(order=idx2).update(order=idx1)
        workload.order = idx2
        workload.save()


class ExerciseTemplate(AbstractExercise):
    workout_templates = models.ForeignKey('workouts.WorkoutTemplate',
                                          related_name='exercises', on_delete=models.CASCADE)

    objects = ExerciseTemplateManager()

    def create_exercise(self, workout):
        return Exercise.from_template(self, workout)


class Exercise(AbstractExercise):
    workouts = models.ForeignKey('workouts.Workout', related_name='exercises', on_delete=models.CASCADE)

    @classmethod
    def from_template(cls, template, workout):
        exercise = cls.objects.create(owner=template.owner, name=template.name,
                                      snames=template.snames, order=len(workout), workouts=workout)
        for workload_template in template.workloads.all():
            workload_template.create_workload(exercise)
        return exercise

    @property
    def is_complete(self):
        return all(workload.is_complete for workload in self.workloads.all())
