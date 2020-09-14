from django.db import models
from .units import UnitsModelMixin, UNITS, KILOGRAMS, POUNDS
from exercises import utils


class AbstractSet(UnitsModelMixin):
    order = models.PositiveSmallIntegerField()
    reps = models.PositiveSmallIntegerField()
    weight = models.FloatField()

    class Meta:
        abstract = True

    def change_units(self, units):
        assert units in UNITS, f'The units must either be `{KILOGRAMS}` or `{POUNDS}` - was given `{units}`'

        if units != self.units:
            if units == KILOGRAMS:
                self.weight = utils.convert_lb_to_kg(self.weight)
            else:
                self.weight = utils.convert_kg_to_lb(self.weight)

            self.units = units
            self.save()


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
                                  reps=template.reps, workload=workload, completed_reps=0, is_complete=False)

    @property
    def is_complete(self):
        return self.completed_reps >= self.reps


class SetTemplateProxy:
    def __init__(self, workload, idx):
        self.__workload = workload
        self.__idx = idx
        self.__set = None

    def __del__(self):
        self.save()

    @property
    def reps(self):
        self._fill_cache()
        return self.__set.reps

    @property
    def weight(self):
        self._fill_cache()
        return self.__set.weight

    @property
    def order(self):
        self._fill_cache()
        return self.__set.order

    @reps.setter
    def reps(self, val):
        if self._is_cached():
            self.__set.reps = val
        else:
            self.__workload.sets.get(order=self.__idx).update(reps=val)

    @weight.setter
    def weight(self, val):
        if self._is_cached():
            self.__set.weight = val
        else:
            self.__workload.sets.get(order=self.__idx).update(weight=val)

    def save(self):
        if self._is_cached():
            assert self.__set.units == self.__workload.units
            self.__set.save()

    def _is_cached(self):
        if self.__set is None:
            return False
        return True

    def _fill_cache(self):
        if not self._is_cached():
            self.__set = self.__workload.sets.get(order=self.__idx)
            assert self.__set.units == self.__workload.units


class SetProxy(SetTemplateProxy):
    @property
    def completed_reps(self):
        self._fill_cache()
        return self.__set.reps()

    @completed_reps.setter
    def completed_reps(self, val):
        if self._is_cached:
            self.__set.completed_reps = val
        else:
            self.__workload.sets.get(order=self.__idx).update(completed_reps=val)

    @property
    def is_complete(self):
        self._fill_cache()
        return self.__set.is_complete
