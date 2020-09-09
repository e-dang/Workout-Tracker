from core.models import OwnedMultiAliasResource


class Equipment(OwnedMultiAliasResource):
    class Meta:
        unique_together = ['name', 'owner']
        verbose_name_plural = 'equipment'
