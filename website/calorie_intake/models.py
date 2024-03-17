from django.conf import settings
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
    )
    
    class Meta:
        db_table = 'component_definitions'
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
    class Meta:
        db_table = 'component_groups'
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
        to = ComponentGroup,
        on_delete = models.CASCADE,
    )
    meal = models.ForeignKey(
        to = 'Meal',
        on_delete = models.CASCADE,
    )
        
    class Meta:
        db_table = 'components'
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
        return ' - '.join(
            self.user.username,
            self.datetime.strftime('%Y-%m-%d %H:%M:%S'),
        )
        
    class Meta:
        db_table = 'meals'
        verbose_name = 'Meal'
