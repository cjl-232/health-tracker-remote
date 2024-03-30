from django.contrib import admin
from .models import ComponentDefinition, ComponentGroup, Component, Meal

@admin.register(ComponentDefinition)
class ComponentDefinitionAdmin(admin.ModelAdmin):
    pass
    
@admin.register(ComponentGroup)
class ComponentGroupAdmin(admin.ModelAdmin):
    pass

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    pass
    
@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    pass