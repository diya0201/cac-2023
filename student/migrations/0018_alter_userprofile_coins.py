# Generated by Django 4.2.6 on 2023-10-29 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("student", "0017_userprofile_high_score_met"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="coins",
            field=models.IntegerField(default=30),
        ),
    ]
