from django.contrib import admin
from .models import WeightTarget

@admin.register(WeightTarget)
class WeightTargetAdmin(admin.ModelAdmin):
    pass
