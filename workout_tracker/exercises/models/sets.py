from django.db import models

from exercises import utils

from .units import KILOGRAMS, POUNDS, UNITS, UnitsModelMixin


class AbstractSet(UnitsModelMixin):
    order = models.PositiveSmallIntegerField()
    reps = models.PositiveSmallIntegerField()
    weight = models.FloatField()

    class Meta:
        abstract = True

    def update(self, reps=None, weight=None, units=None):
        self._change_units(units or self.units)
        self.reps = reps or self.reps
        self.weight = weight or self.weight
        self.save()

    def _change_units(self, units):
        assert units in UNITS, f'The units must either be `{KILOGRAMS}` or `{POUNDS}` - was given `{units}`'

        if units != self.units:
            if units == KILOGRAMS:
                self.weight = utils.convert_lb_to_kg(self.weight)
            else:
                self.weight = utils.convert_kg_to_lb(self.weight)

            self.units = units


class SetTemplate(AbstractSet):
    workload_template = models.ForeignKey('exercises.WorkloadTemplate', related_name='sets', on_delete=models.CASCADE)

    class Meta:
        ordering = ['workload_template', 'order']

    def __str__(self):
        return f'{self.reps} X {self.weight} {self.units}'

    def create_set(self, workload):
        return Set.from_template(self, workload)


class Set(AbstractSet):
    workload = models.ForeignKey('exercises.Workload', related_name='sets', on_delete=models.CASCADE)
    completed_reps = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['workload', 'order']

    def __str__(self):
        return f'{self.completed_reps}/{self.reps} X {self.weight} {self.units}'

    @classmethod
    def from_template(cls, template, workload):
        return Set.objects.create(order=template.order, units=template.units, weight=template.weight,
                                  reps=template.reps, workload=workload, completed_reps=0)

    @property
    def is_complete(self):
        return self.completed_reps >= self.reps
