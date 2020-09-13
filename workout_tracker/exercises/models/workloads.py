from django.db import models
from .units import UnitsModelMixin, KILOGRAMS, POUNDS, UNITS
from .sets import SetTemplate, Set, SetProxy, SetTemplateProxy


class AbstractWorkload(UnitsModelMixin):
    order = models.PositiveSmallIntegerField()

    class Meta:
        abstract = True

    def __str__(self):
        return f'{str(self.movement)} - {", ".join([str(_set) for _set in self.sets.all()])}'

    def __getitem__(self, idx):
        if idx < 0 or idx >= len(self):
            raise KeyError('Index out of range.')

        return self._create_proxy(idx)

    def __delitem__(self, idx):
        try:
            _set = self.sets.get(order=idx)
        except (SetTemplate.DoesNotExist, Set.DoesNotExist):
            raise KeyError('Index out of range.')

        # fix ordering of sets such that they all are adjacent to each other
        self.sets.filter(order__gt=_set.order).update(order=models.F('order') - 1)
        _set.delete()

    def __len__(self):
        return self.sets.all().count()

    def append(self, reps, weight, units=None, order=None):
        _set = self._build_set(reps, weight, units or self.units, order or len(self))
        _set.change_units(self.units)
        assert _set.units == self.units
        _set.save()

    def extend(self, sets):
        for _set in sets:
            self.append(**_set)

    def remove(self, idx):
        del self[idx]

    def change_units(self, units):
        assert units in UNITS, f'The units must either be `{KILOGRAMS}` or `{POUNDS}` - was given `{units}`'

        if units != self.units:
            for _set in self.sets.all():
                assert _set.units == self.units, f'The units for all sets that are part of a workload must be the same'
                _set.change_units(units)

            self.units = units
            self.save()

    def _create_proxy(self, idx):
        raise NotImplementedError

    def _build_set(self, reps, weight, units, order):
        raise NotImplementedError


class WorkloadTemplate(AbstractWorkload):
    movement = models.ForeignKey('movements.Movement', related_name='workload_templates', on_delete=models.CASCADE)
    exercise_template = models.ForeignKey('exercises.ExerciseTemplate',
                                          related_name='workloads', on_delete=models.CASCADE)

    class Meta:
        ordering = ['exercise_template']

    def create_workload(self, exercise):
        Workload.from_template(self, exercise)

    def _create_proxy(self, idx):
        return SetTemplateProxy(self, idx)

    def _build_set(self, reps, weight, units, order):
        return SetTemplate(reps=reps, weight=weight, units=units, order=order, workload_template=self)


class Workload(AbstractWorkload):
    movement = models.ForeignKey('movements.Movement', related_name='workloads', on_delete=models.SET_NULL, null=True)
    exercise = models.ForeignKey('exercises.Exercise', related_name='workloads', on_delete=models.CASCADE)

    class Meta:
        ordering = ['exercise']

    @classmethod
    def from_template(cls, template, exercise):
        workload = Workload.objects.create(order=template.order, units=template.units,
                                           movement=template.movement, exercise=exercise)
        for set_template in template.sets.all():
            set_template.create_set(workload)
        return workload

    @property
    def is_complete(self):
        return all(_set.is_complete for _set in self.sets.all())

    def _create_proxy(self, idx):
        return SetProxy(self, idx)

    def _build_set(self, reps, weight, units, order):
        return SetTemplate(reps=reps, weight=weight, units=units, order=order, workload=self)


class WorkloadTemplateProxy:
    def __init__(self, workload):
        self.__workload = workload

    def __del__(self):
        self.save()

    def __len__(self):
        return len(self.__workload)

    def __delitem__(self, idx):
        del self.__workload[idx]

    def __getitem__(self, idx):
        return self.__workload[idx]

    def __str__(self):
        return str(self.__workload)

    @property
    def units(self):
        return self.__workload.units

    @property
    def order(self):
        return self.__workload.order

    @property
    def movement(self):
        return self.__workload.movement

    @movement.setter
    def movement(self, val):
        self.__workload.movement = val

    def append(self, reps, weight, units):
        self.__workload.append(reps, weight, units)

    def remove(self, idx):
        del self[idx]

    def change_units(self, units):
        self.__workload.change_units(units)

    def save(self):
        self.__workload.save()


class WorkloadProxy(WorkloadTemplateProxy):
    @property
    def is_complete(self):
        return self.__workload.is_complete
