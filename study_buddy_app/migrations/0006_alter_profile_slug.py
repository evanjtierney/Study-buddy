# Generated by Django 4.1.1 on 2022-11-05 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("study_buddy_app", "0005_alter_profile_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile", name="slug", field=models.SlugField(unique=True),
        ),
    ]