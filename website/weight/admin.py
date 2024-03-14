from django.contrib import admin
from .models import WeightObservation, WeightTarget

@admin.register(WeightObservation)
class WeightObservationAdmin(admin.ModelAdmin):
    pass
    
@admin.register(WeightTarget)
class WeightTargetAdmin(admin.ModelAdmin):
    pass
