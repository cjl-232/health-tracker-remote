from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

class ComponentDefinition(models.Model):
    user = models.ForeignKey(
        to = settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
    )
    name = models.CharField(
        max_length = 256,
        blank = False,
    )
    groups = models.ManyToManyField(
        to = 'ComponentGroup',
        blank = True,
    )
    unit_calorie_count = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name + ' (' + self.user.email + ')'
    
    class Meta:
        db_table = 'meals_component_definitions'
        constraints = [
            models.UniqueConstraint(
                fields = ['user', 'name'],
                name = 'component_definition_unique_name_constraint',
            ),
        ]
        indexes = [
            models.Index(fields = ['user']),
        ]
        verbose_name = 'Meal Component Definition'
        
class ComponentGroup(models.Model):
    user = models.ForeignKey(
        to = settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
    )
    name = models.CharField(
        max_length = 256,
        blank = False,
    )
    
    def __str__(self):
        return self.name + ' (' + self.user.email + ')'
    
    class Meta:
        db_table = 'meals_component_groups'
        constraints = [
            models.UniqueConstraint(
                fields = ['user', 'name'],
                name = 'component_group_unique_name_constraint',
            ),
        ]
        indexes = [
            models.Index(fields = ['user']),
        ]
        verbose_name = 'Meal Component Group'

class Component(models.Model):
    definition = models.ForeignKey(
        to = ComponentDefinition,
        on_delete = models.CASCADE,
    )
    quantity = models.DecimalField(
        max_digits = 6,
        decimal_places = 2,
        validators = [
            MinValueValidator(Decimal('0.01')),
        ],
    )
    meal = models.ForeignKey(
        to = 'Meal',
        on_delete = models.CASCADE,
        related_name = 'components',
    )
    
    def __str__(self):
        return self.definition.name + ' x' + '{:.0f}'.format(self.quantity)
        
    def get_calorie_count(self):
        return self.definition.unit_calorie_count * self.quantity
        
    class Meta:
        db_table = 'meals_components'
        verbose_name = 'Meal Component'

class Meal(models.Model):
    user = models.ForeignKey(
        to = settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
    )
    datetime = models.DateTimeField(
        auto_now_add = True,
        verbose_name = 'Meal Datetime',
    )
    
    def __str__(self):
        return ' - '.join([
            self.user.email,
            self.datetime.strftime('%Y-%m-%d %H:%M:%S'),
        ])
        
    def get_calorie_count(self):
        return sum(obj.get_calorie_count() for obj in self.components.all())
        
    class Meta:
        db_table = 'meals_meals'
        verbose_name = 'Meal'
