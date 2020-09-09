import logging

logger = logging.getLogger(__name__)


def percolate(instance, created, model, related_name):
    if created:
        next_level_instance = model.objects.create(name=instance.name, snames=instance.snames)
        try:
            getattr(next_level_instance, related_name).add(instance)
        except AttributeError:
            next_level_instance.delete()
            logger.error(f'Failed to percolate instance {instance} to model {model} using related name {related_name}')


def enforce_no_empty_relationships(instance, related_name, reverse_related_name):
    if hasattr(instance, related_name):
        for related_instance in getattr(instance, related_name).all():
            try:
                if getattr(related_instance, reverse_related_name).all().count() <= 1:
                    related_instance.delete()
            except AttributeError:
                logger.error(f'Failed enforce no empty relationships on {related_instance} when deleting {instance}')
