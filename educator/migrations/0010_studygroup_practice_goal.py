# Generated by Django 4.2.6 on 2023-10-23 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("educator", "0009_studygroup_students_alter_studygroup_educator"),
    ]

    operations = [
        migrations.AddField(
            model_name="studygroup",
            name="practice_goal",
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
