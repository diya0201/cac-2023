# Generated by Django 4.2.6 on 2023-10-22 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("educator", "0006_alter_studygroup_join_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studygroup",
            name="join_code",
            field=models.CharField(
                default="generate_unique_join_code", max_length=6, unique=True
            ),
        ),
    ]