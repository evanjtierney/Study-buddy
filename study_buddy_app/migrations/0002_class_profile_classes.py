# Generated by Django 4.1.1 on 2022-11-05 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("study_buddy_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Class",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("subject", models.CharField(max_length=4)),
                ("catalog_number", models.CharField(max_length=4)),
                ("course_section", models.CharField(max_length=3)),
            ],
        ),
        migrations.AddField(
            model_name="profile",
            name="classes",
            field=models.ManyToManyField(to="study_buddy_app.class"),
        ),
    ]
