from django.db import models

KILOGRAMS = 'kg'
POUNDS = 'lb'
UNITS = (KILOGRAMS, POUNDS)
UNIT_CHOICES = (
    (KILOGRAMS, 'Kilograms'),
    (POUNDS, 'Pounds')
)


class UnitsModelMixin(models.Model):
    units = models.CharField(max_length=2, choices=UNIT_CHOICES, default=POUNDS)

    class Meta:
        abstract = True
