# Generated by Django 5.1.1 on 2024-09-11 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("AMS", "0004_alter_student_ntfy_topic"),
    ]

    operations = [
        migrations.AddField(
            model_name="attendance",
            name="last_run",
            field=models.DateField(auto_now=True),
        ),
    ]
