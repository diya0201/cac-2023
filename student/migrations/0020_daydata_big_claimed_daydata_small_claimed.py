# Generated by Django 4.2.6 on 2023-10-29 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("student", "0019_alter_userprofile_coins"),
    ]

    operations = [
        migrations.AddField(
            model_name="daydata",
            name="big_claimed",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="daydata",
            name="small_claimed",
            field=models.BooleanField(default=False),
        ),
    ]