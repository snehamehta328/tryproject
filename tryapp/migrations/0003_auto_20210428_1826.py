# Generated by Django 3.2 on 2021-04-28 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tryapp', '0002_alter_account_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='hide_email',
        ),
        migrations.AlterField(
            model_name='account',
            name='password',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterModelTable(
            name='account',
            table='usersingupp',
        ),
    ]