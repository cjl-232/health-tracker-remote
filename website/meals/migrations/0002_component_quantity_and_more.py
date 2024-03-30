# Generated by Django 5.0.2 on 2024-03-21 00:39

import django.core.validators
import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='quantity',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='componentdefinition',
            name='unit_calorie_count',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='component',
            name='meal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='components', to='meals.meal'),
        ),
    ]
