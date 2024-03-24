# Generated by Django 5.0.2 on 2024-03-18 00:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ComponentGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Meal Component Group',
                'db_table': 'meals_component_groups',
            },
        ),
        migrations.CreateModel(
            name='ComponentDefinition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(to='meals.componentgroup')),
            ],
            options={
                'verbose_name': 'Meal Component Definition',
                'db_table': 'meals_component_definitions',
            },
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='Meal Datetime')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Meal',
                'db_table': 'meals_meals',
            },
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('definition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meals.componentgroup')),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meals.meal')),
            ],
            options={
                'verbose_name': 'Meal Component',
                'db_table': 'meals_components',
            },
        ),
        migrations.AddIndex(
            model_name='componentgroup',
            index=models.Index(fields=['user'], name='meals_compo_user_id_737247_idx'),
        ),
        migrations.AddConstraint(
            model_name='componentgroup',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='component_group_unique_name_constraint'),
        ),
        migrations.AddIndex(
            model_name='componentdefinition',
            index=models.Index(fields=['user'], name='meals_compo_user_id_108d5d_idx'),
        ),
        migrations.AddConstraint(
            model_name='componentdefinition',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='component_definition_unique_name_constraint'),
        ),
    ]