# Generated by Django 4.0.3 on 2022-03-03 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_alter_todoitem_is_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoitem',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
