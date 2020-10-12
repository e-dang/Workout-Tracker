from django.db import models


class ExerciseTemplateRelatedManager(models.Manager):
    def create(self, movement, units, order, sets=None):
        exercise_template = self.model(owner=self.instance.owner, name=movement.name,
                                       snames=movement.snames, order=order)
        exercise_template.save()
        exercise_template.workloads.create(movement, units, 0, sets=sets)
        return exercise_template


class ExerciseTemplateManager(models.Manager):

    def create(self, owner, name, snames, order, workout_templates, workloads=None):
        exercise_template = self.model(
            owner=owner,
            name=name,
            snames=snames,
            order=order,
            workout_templates=workout_templates
        )
        exercise_template.save()
        exercise_template.extend(workloads or [])
        return exercise_template


class WorkloadTemplateRelatedManager(models.Manager):
    use_for_related_fields = True

    def create(self, movement, units, order, sets=None, **kwargs):
        workload = super().create(movement=movement, units=units, order=order, **kwargs)
        workload.extend(sets or [])
        return workload


class WorkloadRelatedManager(models.Manager):
    use_for_related_fields = True

    def create(self, movement, units, order, sets=None, **kwargs):
        workload = super().create(movement=movement, units=units, order=order, **kwargs)
        workload.extend(sets or [])
        return workload
