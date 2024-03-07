# Generated by Django 5.0.2 on 2024-02-21 23:19

import colorfield.fields
import django.core.validators
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weight', '0007_userinfo_delete_weightbaseline_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='weighttarget',
            name='colour',
            field=colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=25, samples=None),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='baseline_weight',
            field=models.DecimalField(db_comment='Baseline weight in kilograms', decimal_places=1, max_digits=4, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Baseline Weight (kg)'),
        ),
        migrations.AddConstraint(
            model_name='weighttarget',
            constraint=models.UniqueConstraint(fields=('user', 'value'), name='unique_value_constraint'),
        ),
    ]