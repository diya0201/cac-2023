# Generated by Django 4.2.6 on 2023-10-22 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("educator", "0002_studygroup_join_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studygroup",
            name="join_code",
            field=models.CharField(default="RQEOSI", max_length=6),
        ),
    ]
