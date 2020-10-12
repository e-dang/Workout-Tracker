from django.db import models


class WorkoutTemplateManager(models.Manager):

    def create(self, owner, name, exercises=None):
        workout_template = self.model(
            owner=owner,
            name=name,
        )

        workout_template.save()
        if exercises is not None:
            workout_template.extend(exercises)

        return workout_template
