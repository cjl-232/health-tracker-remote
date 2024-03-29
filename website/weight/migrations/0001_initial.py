# Generated by Django 5.0.2 on 2024-03-07 02:29

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WeightObservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(db_comment='Weight in kilograms at the time of entry', decimal_places=1, max_digits=4, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Weight (kg)')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'weight_observations',
            },
        ),
        migrations.CreateModel(
            name='WeightTarget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('value', models.DecimalField(db_comment='Target weight in kilograms', decimal_places=1, max_digits=4, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Weight (kg)')),
                ('colour', models.CharField(default='#000000', max_length=256, validators=[django.core.validators.RegexValidator(message='Enter a valid hex code.', regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Weight Target',
                'db_table': 'weight_targets',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('baseline_weight', models.DecimalField(db_comment='Baseline weight in kilograms', decimal_places=1, max_digits=4, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Baseline Weight (kg)')),
                ('baseline_weight_datetime', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Baseline Weight Datetime')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'weight_user_info',
                'indexes': [models.Index(fields=['user'], name='weight_user_user_id_80a1a6_idx')],
            },
        ),
        migrations.AddConstraint(
            model_name='userinfo',
            constraint=models.UniqueConstraint(fields=('user',), name='unique_user_constraint'),
        ),
        migrations.AddIndex(
            model_name='weightobservation',
            index=models.Index(fields=['user', 'datetime'], name='weight_obse_user_id_d0120b_idx'),
        ),
        migrations.AddIndex(
            model_name='weighttarget',
            index=models.Index(fields=['user'], name='weight_targ_user_id_42f53e_idx'),
        ),
        migrations.AddConstraint(
            model_name='weighttarget',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='unique_name_constraint'),
        ),
        migrations.AddConstraint(
            model_name='weighttarget',
            constraint=models.UniqueConstraint(fields=('user', 'value'), name='unique_value_constraint'),
        ),
    ]
