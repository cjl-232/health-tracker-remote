# Generated by Django 5.0.2 on 2024-02-13 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={},
        ),
        migrations.AlterModelTableComment(
            name='customuser',
            table_comment='User accounts',
        ),
        migrations.AlterModelTable(
            name='customuser',
            table='users',
        ),
    ]