from django.db import models


class ExerciseTemplateManager(models.Manager):

    def create(self, owner, name, snames, workloads=None):
        exercise_template = self.model(
            owner=owner,
            name=name,
            snames=snames
        )
        exercise_template.save()
        if workloads is not None:
            exercise_template.extend(workloads)
        return exercise_template


class WorkloadTemplateRelatedManager(models.Manager):
    use_for_related_fields = True

    def create(self, movement, units, order, sets=None):
        return _create_workload_helper(self.model, movement, units, order, sets, exercise_template=self.instance)


class WorkloadRelatedManager(models.Manager):
    use_for_related_fields = True

    def create(self, movement, units, order, sets=None):
        return _create_workload_helper(self.model, movement, units, order, sets, exercise=self.instance)


def _create_workload_helper(model, movement, units, order, sets, **kwargs):
    workload = model(movement=movement, units=units, order=order, **kwargs)
    if sets is not None:
        workload.extend(sets)
    return workload
