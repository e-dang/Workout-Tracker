from rest_framework import serializers

from core.serializers import OwnedMultiAliasResourceSerializer, extend_fields

from .models import ExerciseTemplate, SetTemplate, WorkloadTemplate, Set, Workload, Exercise
from movements.serializers import MovementSerializer


class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ['order', 'reps', 'completed_reps', 'weight']


class WorkloadSerializer(serializers.ModelSerializer):
    sets = SetSerializer(many=True)
    movement = MovementSerializer()

    class Meta:
        model = Workload
        fields = ['order', 'movement', 'sets', 'units']


class ExerciseSerializer(serializers.ModelSerializer):
    workloads = WorkloadSerializer(many=True)

    class Meta:
        model = Exercise
        fields = ['name', 'order', 'workloads']

    def update(self, instance, validated_data):
        _update_exercise(instance, validated_data)


def _update_set(instance, validated_data):
    instance.completed_reps = validated_data.get('completed_reps')
    instance.save()
    return instance


def _update_workload(instance, validated_data):
    for set_data in validated_data.get('sets', []):
        _update_set(instance[set_data['order']], set_data)
    instance.save()
    return instance


def _update_exercise(instance, validated_data):
    for workload_data in validated_data.get('workloads', []):
        _update_workload(instance[workload_data['order']], workload_data)
    instance.save()
    return instance


class SetTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetTemplate
        fields = ['order', 'reps', 'weight']

    def update(self, instance, validated_data):
        return _update_set_templates(instance, validated_data)


class WorkloadTemplateSerializer(serializers.ModelSerializer):
    sets = SetTemplateSerializer(many=True)

    class Meta:
        model = WorkloadTemplate
        fields = ['order', 'movement', 'sets', 'units']

    def update(self, instance, validated_data):
        return _update_workload_templates(instance, validated_data)


class ExerciseTemplateSerializer(OwnedMultiAliasResourceSerializer):
    workloads = WorkloadTemplateSerializer(many=True)

    class Meta:
        model = ExerciseTemplate
        fields = extend_fields(OwnedMultiAliasResourceSerializer, ['order', 'workout_templates', 'workloads'])
        extra_kwargs = {
            'url': {'view_name': 'exercise-detail', 'lookup_field': 'pk'},
            'workout_templates': {'view_name': 'workout-template-detail', 'lookup_field': 'pk'}
        }

    def create(self, validated_data):
        return ExerciseTemplate.objects.create(
            owner=validated_data['owner'],
            name=validated_data['name'],
            snames=validated_data['snames'],
            order=validated_data['order'],
            workout_templates=validated_data['workout_templates'],
            workloads=validated_data.get('workloads', [])
        )

    def update(self, instance, validated_data):
        return _update_exercise_templates(instance, validated_data)


def _update_set_templates(instance, validated_data):
    instance.reps = validated_data.get('reps', instance.reps)
    instance.weight = validated_data.get('weight', instance.weight)
    instance.save()
    return instance


def _update_workload_templates(instance, validated_data):
    instance.movement = validated_data.get('movement', instance.movement)
    instance.change_units(validated_data.get('units', instance.units))
    for set_data in validated_data.get('sets', []):
        _update_set_templates(instance[set_data['order']], set_data)
    instance.save()
    return instance


def _update_exercise_templates(instance, validated_data):
    instance.name = validated_data.get('name', instance.name)
    instance.snames = validated_data.get('snames', instance.snames)
    for workload_data in validated_data.get('workloads', []):
        _update_workload_templates(instance[workload_data['order']], workload_data)
    instance.save()
    return instance
