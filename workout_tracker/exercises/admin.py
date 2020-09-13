from django.contrib import admin
from .models import ExerciseTemplate, Exercise, WorkloadTemplate, Workload, SetTemplate, Set


class ExerciseTemplateAdmin(admin.ModelAdmin):
    pass


class ExerciseAdmin(admin.ModelAdmin):
    pass


class WorkloadTemplateAdmin(admin.ModelAdmin):
    pass


class WorkloadAdmin(admin.ModelAdmin):
    pass


class SetTemplateAdmin(admin.ModelAdmin):
    pass


class SetAdmin(admin.ModelAdmin):
    pass


admin.site.register(ExerciseTemplate, ExerciseTemplateAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(WorkloadTemplate, WorkloadTemplateAdmin)
admin.site.register(Workload, WorkloadAdmin)
admin.site.register(SetTemplate, SetTemplateAdmin)
admin.site.register(Set, SetAdmin)
