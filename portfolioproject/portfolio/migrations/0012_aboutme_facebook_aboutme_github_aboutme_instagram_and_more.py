# Generated by Django 4.2.11 on 2024-08-05 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0011_aboutme_video_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="aboutme",
            name="facebook",
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="aboutme",
            name="github",
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="aboutme",
            name="instagram",
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="aboutme",
            name="linkedin",
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
