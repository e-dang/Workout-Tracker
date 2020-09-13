import factory
from django.db.models.signals import post_save, pre_delete

from exercises.models import UNITS

TEST_PASSWORD = 'strong-test-pass123'


class UserFactory(factory.django.DjangoModelFactory):

    username = factory.Sequence(lambda x: f'username{x}')
    email = factory.Faker('email')
    password = TEST_PASSWORD
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    is_staff = False
    is_superuser = False

    class Meta:
        model = 'users.User'

    class Params:
        inactive = factory.Trait(
            is_active=False,
            is_staff=False,
            is_superuser=False
        )
        active = factory.Trait(
            is_active=True,
            is_staff=False,
            is_superuser=False
        )
        admin = factory.Trait(
            is_active=True,
            is_staff=True,
            is_superuser=False
        )
        superuser = factory.Trait(
            is_active=True,
            is_staff=True,
            is_superuser=True
        )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)

    @factory.post_generation
    def equipment(self, create, counts, **kwargs):
        if not create:
            return

        if counts:
            for _ in range(counts):
                self.equipments.add(EquipmentFactory())

    @factory.post_generation
    def movements(self, create, counts, **kwargs):
        if not create:
            return

        if counts:
            for _ in range(counts):
                self.movements.add(MovementFactory())


@factory.django.mute_signals(post_save)
@factory.django.mute_signals(pre_delete)
class MuscleGroupingFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda x: f'back{x}')
    snames = factory.Sequence(lambda x: [f'Back{x}'])

    class Meta:
        model = 'muscles.MuscleGrouping'

    @factory.post_generation
    def muscles(self, create, counts, **kwargs):
        if not create:
            return

        if counts:
            for _ in range(counts):
                self.muscles.add(MuscleFactory(subportions=1))


@factory.django.mute_signals(post_save)
@factory.django.mute_signals(pre_delete)
class MuscleFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda x: f'traps{x}')
    snames = factory.Sequence(lambda x: [f'Traps{x}', f'trap{x}'])

    class Meta:
        model = 'muscles.Muscle'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        muscle = manager.create(*args, **kwargs)
        grouping = MuscleGroupingFactory()
        grouping.muscles.add(muscle)
        return muscle

    @factory.post_generation
    def subportions(self, create, counts, **kwargs):
        if not create:
            return

        if counts:
            for _ in range(counts):
                self.subportions.add(MuscleSubportionFactory())


@factory.django.mute_signals(post_save)
@factory.django.mute_signals(pre_delete)
class MuscleSubportionFactory(factory.django.DjangoModelFactory):

    name = factory.Sequence(lambda x: f'upper traps{x}')
    snames = factory.Sequence(lambda x: [f'Upper traps{x}', f'uppertraps{x}'])

    class Meta:
        model = 'muscles.MuscleSubportion'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        subportion = manager.create(*args, **kwargs)
        muscle = MuscleFactory()
        muscle.subportions.add(subportion)
        return subportion


class EquipmentFactory(factory.django.DjangoModelFactory):
    owner = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda x: f'barbell{x}')
    snames = factory.Sequence(lambda x: [f'Barbell{x}', f'bar bell{x}'])

    class Meta:
        model = 'equipment.Equipment'


class MovementFactory(factory.django.DjangoModelFactory):
    owner = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda x: f'bench press{x}')
    snames = factory.Sequence(lambda x: [f'benchpress{x}', f'Benchpress{x}'])
    equipment = factory.SubFactory(EquipmentFactory)
    description = factory.Faker('text')

    class Meta:
        model = 'movements.Movement'

    @factory.post_generation
    def muscles(self, create, counts, **kwargs):
        if not create:
            return

        if counts:
            for _ in range(counts):
                self.muscles.add(MuscleGroupingFactory())


class ExerciseTemplateFactory(factory.django.DjangoModelFactory):
    owner = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda x: f'bench press{x}')
    snames = factory.Sequence(lambda x: [f'benchpress{x}', f'Benchpress{x}'])

    class Meta:
        model = 'exercises.ExerciseTemplate'

    @factory.post_generation
    def workloads(self, create, count, **kwargs):
        if not create:
            return

        if count:
            for _ in range(count):
                WorkloadTemplateFactory(exercise_template=self, movement=MovementFactory(), **kwargs)


class ExerciseFactory(factory.django.DjangoModelFactory):
    owner = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda x: f'bench press{x}')
    snames = factory.Sequence(lambda x: [f'benchpress{x}', f'Benchpress{x}'])

    class Meta:
        model = 'exercises.Exercise'

    @factory.post_generation
    def workloads(self, create, count, **kwargs):
        if not create:
            return

        if count:
            for _ in range(count):
                WorkloadFactory(exercise=self, movement=MovementFactory(), **kwargs)


class WorkloadTemplateFactory(factory.django.DjangoModelFactory):
    movement = factory.SubFactory(MovementFactory)
    exercise_template = factory.SubFactory(ExerciseTemplateFactory)
    units = factory.Iterator(UNITS)

    class Meta:
        model = 'exercises.WorkloadTemplate'

    @factory.post_generation
    def sets(self, create, count, **kwargs):
        if not create:
            return

        if count:
            for _ in range(count):
                SetTemplateFactory.create(workload_template=self)


class WorkloadFactory(factory.django.DjangoModelFactory):
    movement = factory.SubFactory(MovementFactory)
    exercise = factory.SubFactory(ExerciseFactory)
    units = factory.Iterator(UNITS)

    class Meta:
        model = 'exercises.Workload'

    @factory.post_generation
    def sets(self, create, count, **kwargs):
        if not create:
            return

        if count:
            for _ in range(count):
                SetFactory.create(workload=self)


class AbstractSetFactory(factory.django.DjangoModelFactory):
    reps = factory.Faker('pyint', min_value=0, max_value=50)
    weight = factory.Faker('pyfloat', min_value=0, max_value=1000)


class SetTemplateFactory(AbstractSetFactory):
    workload_template = factory.SubFactory(WorkloadTemplateFactory)
    units = factory.LazyAttribute(lambda o: o.workload_template.units)

    class Meta:
        model = 'exercises.SetTemplate'


class SetFactory(AbstractSetFactory):
    workload = factory.SubFactory(WorkloadFactory)
    units = factory.LazyAttribute(lambda o: o.workload.units)

    class Meta:
        model = 'exercises.Set'
