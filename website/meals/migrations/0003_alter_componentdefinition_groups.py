# Generated by Django 5.0.2 on 2024-03-21 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0002_component_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componentdefinition',
            name='groups',
            field=models.ManyToManyField(blank=True, to='meals.componentgroup'),
        ),
    ]
