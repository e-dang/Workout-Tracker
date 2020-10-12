from core.serializers import OwnedMultiAliasResourceSerializer, extend_fields
from rest_framework import serializers
from .models import WorkoutTemplate, Workout

from exercises.serializers import ExerciseTemplateSerializer, ExerciseSerializer, _update_exercise


class WorkoutTemplateSerializer(OwnedMultiAliasResourceSerializer):
    exercises = ExerciseTemplateSerializer(many=True)

    class Meta:
        model = WorkoutTemplate
        fields = extend_fields(OwnedMultiAliasResourceSerializer, ['exercises'])
        read_only_fields = ['snames']
        extra_kwargs = {
            'url': {'view_name': 'workout-template-detail', 'lookup_field': 'pk'},
            'exercises': {'view_name': 'exercise-template-detail', 'lookup_field': 'pk'}
        }

    def create(self, validated_data):
        return WorkoutTemplate.objects.create(
            owner=validated_data['owner'],
            name=validated_data['name'],
            exercises=validated_data.get('exercises', None)
        )


class WorkoutSerializer(OwnedMultiAliasResourceSerializer):
    exercises = ExerciseSerializer(many=True)

    class Meta:
        model = Workout
        fields = extend_fields(OwnedMultiAliasResourceSerializer, ['exercises', 'time', 'is_complete'])
        extra_kwargs = {
            'url': {'view_name': 'workout-detail', 'lookup_field': 'pk'}
        }

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.snames = validated_data.get('snames', instance.snames)
        instance.time = validated_data.get('time', instance.time)
        instance.is_complete = validated_data.get('is_complete', instance.is_complete)
        for exercise_data in validated_data.get('exercises', []):
            _update_exercise(instance[exercise_data['order']], exercise_data)
        instance.save()
        return instance
