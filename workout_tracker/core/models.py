from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf import settings


class MultiAliasResource(models.Model):
    """
    Abstract Model to be inherited by resources that can forseeably have multiple names that they commonly go by. For
    example, the shoulder muscle is commonly refered to as both "shoulder", "delt", and "deltoid". This abstract Model
    adds the aliases field and associated __str__ and __repr__ methods to that Model. The alias at the first index in
    the aliases field holds special meaning, as this is the name that will be used to represent the resource.
    """
    name = models.CharField(max_length=100)
    snames = ArrayField(models.CharField(max_length=100))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name.capitalize()

    def __repr__(self):
        return '\n\t'.join([f'Name: {self.__str__()}'] + self._capitalize_snames())

    @property
    def aliases(self):
        return [self.__str__()] + self._capitalize_snames()

    def _capitalize_snames(self):
        return [name.capitalize() for name in self.snames]


class OwnedMultiAliasResource(MultiAliasResource):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s',
                              related_query_name='%(class)s', on_delete=models.CASCADE)

    class Meta:
        abstract = True
