# Generated by Django 4.2.6 on 2023-10-29 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("student", "0016_alter_joingroup_join_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="high_score_met",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
