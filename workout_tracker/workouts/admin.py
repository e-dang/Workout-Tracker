from django.contrib import admin

from .models import WorkoutTemplate, Workout


class WorkoutTemplateAdmin(admin.ModelAdmin):
    pass


class WorkoutAdmin(admin.ModelAdmin):
    pass


admin.site.register(WorkoutTemplate, WorkoutTemplateAdmin)
admin.site.register(Workout, WorkoutAdmin)
