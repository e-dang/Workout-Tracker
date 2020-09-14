from rest_framework import serializers

from core.serializers import OwnedMultiAliasResourceSerializer, extend_fields

from .models import ExerciseTemplate, SetTemplate, WorkloadTemplate


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
        fields = extend_fields(OwnedMultiAliasResourceSerializer, ['workloads'])

    def create(self, validated_data):
        return ExerciseTemplate.objects.create(
            owner=validated_data['owner'],
            name=validated_data['name'],
            snames=validated_data['snames'],
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
