from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

class UserInfo(models.Model):
    
    user = models.ForeignKey(
        to = settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
    )
    baseline_weight = models.DecimalField(
        max_digits = 4,
        decimal_places = 1,
        db_comment = 'Baseline weight in kilograms',
        validators = [
            MinValueValidator(Decimal('0.01')),
        ],
        verbose_name = 'Baseline Weight (kg)',
    )
    
    class Meta:
        db_table = 'weight_user_info'
        constraints = [
            models.UniqueConstraint(
                fields = ['user'],
                name = 'unique_user_constraint',
            ),
        ]
        indexes = [
            models.Index(fields = ['user']),
        ]
        
class WeightObservation(models.Model):
    
    user = models.ForeignKey(
        to = settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
    )
    weight = models.DecimalField(
        max_digits = 4,
        decimal_places = 1,
        db_comment = 'Weight in kilograms at the time of entry',
        validators = [
            MinValueValidator(Decimal('0.01')),
        ],
        verbose_name = 'Weight (kg)',
    )
    datetime = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        db_table = 'weight_observations'
        indexes = [
            models.Index(fields = ['user', 'datetime']),
        ]
        
class WeightTarget(models.Model):

    user = models.ForeignKey(
        to = settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
    )
    name = models.CharField(
        max_length = 256,
        blank = False,
    )
    value = models.DecimalField(
        max_digits = 4,
        decimal_places = 1,
        db_comment = 'Target weight in kilograms',
        validators = [
            MinValueValidator(Decimal('0.01')),
        ],
        verbose_name = 'Weight (kg)',
    )
    
    class Meta:
        db_table = 'weight_targets'
        constraints = [
            models.UniqueConstraint(
                fields = ['user', 'name'],
                name = 'unique_name_constraint',
            ),
        ]
        indexes = [
            models.Index(fields = ['user']),
        ]