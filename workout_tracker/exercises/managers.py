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
