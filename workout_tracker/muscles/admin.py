from django.contrib import admin
from .models import MuscleSubportion, Muscle, MuscleGrouping


class MuscleSubportionAdmin(admin.ModelAdmin):
    class Meta:
        model = MuscleSubportion


class MuscleAdmin(admin.ModelAdmin):
    class Meta:
        model = Muscle


class MuscleGroupingAdmin(admin.ModelAdmin):
    class Meta:
        model = MuscleGrouping


admin.site.register(MuscleSubportion, MuscleSubportionAdmin)
admin.site.register(Muscle, MuscleAdmin)
admin.site.register(MuscleGrouping, MuscleGroupingAdmin)
