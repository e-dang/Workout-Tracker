from django.db import models
from core.models import OwnedMultiAliasResource
from datetime import timedelta
from exercises.models import ExerciseTemplate, Exercise
from .managers import WorkoutTemplateManager


class AbstractWorkout(OwnedMultiAliasResource):
    class Meta:
        abstract = True

    def __getitem__(self, idx):
        if (exercise := self.get(idx)) is None:
            raise KeyError('Index out of range.')
        return exercise

    def __delitem__(self, idx):
        exercise = self[idx]
        self.exercises.filter(order__gt=exercise.order).update(order=models.F('order') - 1)
        exercise.delete()

    def __len__(self):
        return self.exercises.all().count()

    def get(self, idx, default=None):
        try:
            return self.exercises.get(order=idx)
        except (ExerciseTemplate.DoesNotExist, Exercise.DoesNotExist):
            return default

    def append(self, movement, units, order=None, sets=None):
        self.exercises.create(movement, units, order=order or len(self), sets=sets)

    def extend(self, exercises):
        for exercise in exercises:
            self.append(**exercise)

    def remove(self, idx):
        del self[idx]

    def swap_exercises(self, idx1, idx2):
        exercise = self.exercises.get(order=idx1)
        self.exercises.filter(order=idx2).update(order=idx1)
        exercise.order = idx2
        exercise.save()


class WorkoutTemplate(AbstractWorkout):

    objects = WorkoutTemplateManager()

    def create_workout(self):
        return Workout.from_template(self)


class Workout(AbstractWorkout):
    is_complete = models.BooleanField(default=False)
    time = models.DurationField(default=timedelta)

    @classmethod
    def from_template(cls, template):
        workout = cls.objects.create(owner=template.owner, name=template.name, snames=template.snames)
        for exercise_template in template.exercises.all():
            exercise_template.create_exercise(workout)
        return workout
