# Generated by Django 4.2 on 2023-05-10 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("book_api", "0008_alter_publisher_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="publisher",
            name="text",
            field=models.CharField(default="text", max_length=100),
        ),
    ]