# Generated by Django 4.1.1 on 2022-11-05 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("study_buddy_app", "0004_alter_profile_class"),
    ]

    operations = [
        migrations.RemoveField(model_name="profile", name="Class",),
        migrations.AddField(
            model_name="profile",
            name="classes",
            field=models.ManyToManyField(to="study_buddy_app.class"),
        ),
    ]
