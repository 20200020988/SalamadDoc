# Generated by Django 4.2.1 on 2023-05-21 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_appointment_group_id_appointment_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='group_id',
            new_name='doctor_id',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='user_id',
        ),
    ]
