# Generated by Django 4.2.11 on 2024-07-29 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0008_experience_order_number_qualification_order_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="portfolio",
            name="name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
