from django.db import models

from .sets import Set, SetTemplate
from .units import KILOGRAMS, POUNDS, UNITS, UnitsModelMixin


class AbstractWorkload(UnitsModelMixin):
    order = models.PositiveSmallIntegerField()

    class Meta:
        abstract = True

    def __str__(self):
        return f'{str(self.movement)} - {", ".join([str(_set) for _set in self.sets.all()])}'

    def __getitem__(self, idx):
        if (s := self.get(idx)) is None:
            raise KeyError('Index out of range.')
        return s

    def __delitem__(self, idx):
        s = self[idx]

        # fix ordering of sets such that they all are adjacent to each other
        self.sets.filter(order__gt=s.order).update(order=models.F('order') - 1)
        s.delete()

    def __len__(self):
        return self.sets.all().count()

    def get(self, idx, default=None):
        try:
            return self.sets.get(order=idx)
        except (SetTemplate.DoesNotExist, Set.DoesNotExist):
            return default

    def update(self, movement=None, units=None):
        self._change_units(units or self.units)
        self.movement = movement or self.movement
        if movement is not None or units is not None:
            self.save()

    def append(self, reps, weight, units=None, order=None):
        s = self._build_set(reps, weight, units or self.units, order or len(self))
        s._change_units(self.units)
        assert s.units == self.units
        s.save()

    def extend(self, sets):
        for s in sets:
            self.append(**s)

    def remove(self, idx):
        del self[idx]

    def swap_sets(self, idx1, idx2):
        s1 = self.sets.get(order=idx1)
        self.sets.filter(order=idx2).update(order=idx1)
        s1.order = idx2
        s1.save()

    def _change_units(self, units):
        assert units in UNITS, f'The units must either be `{KILOGRAMS}` or `{POUNDS}` - was given `{units}`'

        if units != self.units:
            for s in self.sets.all():
                assert s.units == self.units, f'The units for all sets that are part of a workload must be the same'
                s._change_units(units)

            self.units = units

    def _build_set(self, reps, weight, units, order):
        raise NotImplementedError


class WorkloadTemplate(AbstractWorkload):
    movement = models.ForeignKey('movements.Movement', related_name='workload_templates', on_delete=models.CASCADE)
    exercise_template = models.ForeignKey('exercises.ExerciseTemplate',
                                          related_name='workloads', on_delete=models.CASCADE)

    class Meta:
        ordering = ['exercise_template']

    def create_workload(self, exercise):
        return Workload.from_template(self, exercise)

    def _build_set(self, reps, weight, units, order):
        return SetTemplate(reps=reps, weight=weight, units=units, order=order, workload_template=self)


class Workload(AbstractWorkload):
    movement = models.ForeignKey('movements.Movement', related_name='workloads', on_delete=models.SET_NULL, null=True)
    exercise = models.ForeignKey('exercises.Exercise', related_name='workloads', on_delete=models.CASCADE)

    class Meta:
        ordering = ['exercise']

    @classmethod
    def from_template(cls, template, exercise):
        workload = cls.objects.create(order=template.order, units=template.units,
                                      movement=template.movement, exercise=exercise)
        for set_template in template.sets.all():
            set_template.create_set(workload)
        return workload

    @property
    def is_complete(self):
        return all(s.is_complete for s in self.sets.all())

    def _build_set(self, reps, weight, units, order):
        return Set(reps=reps, weight=weight, units=units, order=order, workload=self)
