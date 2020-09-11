from django.contrib import admin
from .models import Movement


class MovementAdmin(admin.ModelAdmin):
    class Meta:
        model = Movement


admin.site.register(Movement, MovementAdmin)
