# Generated by Django 4.1.2 on 2023-12-01 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0003_remove_book_genre_book_genre"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="description",
            field=models.CharField(
                blank=True, max_length=50000, verbose_name="Описание"
            ),
        ),
    ]
