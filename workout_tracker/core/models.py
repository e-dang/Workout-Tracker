from django.db import models
from django.contrib.postgres.fields import ArrayField


class MultiAliasResource(models.Model):
    """
    Abstract Model to be inherited by resources that can forseeably have multiple names that they commonly go by. For
    example, the shoulder muscle is commonly refered to as both "shoulder", "delt", and "deltoid". This abstract Model
    adds the aliases field and associated __str__ and __repr__ methods to that Model. The alias at the first index in
    the aliases field holds special meaning, as this is the name that will be used to represent the resource.
    """
    name = models.CharField(max_length=100)
    snames = ArrayField(models.CharField(max_length=100))

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def __repr__(self):
        return '\n\t'.join([f'Name: {self.name}'] + self.snames)

    @property
    def aliases(self):
        return [self.name] + self.snames
