from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils import timezone

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
    baseline_weight_datetime = models.DateTimeField(
        default = timezone.now,
        editable = False,
        verbose_name = 'Baseline Weight Datetime',
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
    value = models.DecimalField(
        max_digits = 4,
        decimal_places = 1,
        db_comment = 'Weight in kilograms at the time of entry',
        validators = [
            MinValueValidator(Decimal('0.01')),
        ],
        verbose_name = 'Weight (kg)',
    )
    datetime = models.DateTimeField(
        default = timezone.now,
        editable = False,
        verbose_name = 'Observation Datetime',
    )
    
    def __str__(self):
        return ' - '.join([
            self.datetime.strftime('%Y-%m-%d'),
            '{:.1f}'.format(self.value) + 'kg'
        ])
    
    def get_label(self):
        return self.__str__()
    
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
    colour = models.CharField(
        max_length = 256,
        blank = False,
        default='#000000',
        validators = [
            RegexValidator(
                regex = '^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message = 'Enter a valid hex code.',
            ),
        ],
    )
    
    def __str__(self):
        return self.name + ' - ' + '{:.1f}'.format(self.value) + 'kg'
        
    def get_label(self):
        return self.__str__()
        
    def calculate_progress(self, baseline_weight, current_weight):
        format_string = '{:.1%}'
        if self.value < current_weight < baseline_weight:
            current_progress = baseline_weight - current_weight
            desired_progress = baseline_weight - self.value
            return format_string.format(current_progress / desired_progress)
        elif self.value >= current_weight:
            return format_string.format(1.0)
        else:
            return format_string.format(0.0)
    
    class Meta:
        db_table = 'weight_targets'
        constraints = [
            models.UniqueConstraint(
                fields = ['user', 'name'],
                name = 'unique_name_constraint',
            ),
            models.UniqueConstraint(
                fields = ['user', 'value'],
                name = 'unique_value_constraint',
            ),
        ]
        indexes = [
            models.Index(fields = ['user']),
        ]
        verbose_name = 'Weight Target'