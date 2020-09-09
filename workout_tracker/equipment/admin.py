from django.contrib import admin
from .models import Equipment


class EquipmentAdmin(admin.ModelAdmin):
    class Meta:
        model = Equipment


admin.site.register(Equipment, EquipmentAdmin)
