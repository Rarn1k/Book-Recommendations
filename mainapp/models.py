from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Genre(models.Model):

    name = models.CharField(max_length=50, verbose_name='Название жанра')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Book(models.Model):

    title = models.CharField(max_length=1000, verbose_name='Название книги')
    authors = models.CharField(max_length=1000, verbose_name='Авторы')
    image_url = models.URLField(verbose_name="Изображение")
    average_rating = models.FloatField(verbose_name="Средний рейтинг")
    rating_counts = models.PositiveIntegerField(verbose_name="Количество оценок")
    description = models.CharField(max_length=50000, blank=True, verbose_name="Описание")
    genre = models.ManyToManyField(Genre, verbose_name='Жанр', related_name="book", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class UserRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_rating", verbose_name="Пользователь")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="user_rating", verbose_name="Книга")
    book_rating = models.IntegerField(verbose_name="Оценка")

    def __str__(self):
        return (
            self.user.username.capitalize()
            + "- "
            + self.book.name
            + "  - "
            + str(self.book_rating)
        )


class SaveForLater(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_save", verbose_name="Пользователь")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="user_save", verbose_name="Книга")

    def __str__(self):
        return self.user.username.capitalize() + "- " + self.book.title


@receiver(post_save, sender=UserRating)
def update_book_rating(sender, instance, **kwargs):
    book = instance.book
    total_ratings = book.rating_counts

    #если пользователь уже оценивал эту книгу
    previous_rating = UserRating.objects.filter(book=book, user=instance.user).first()

    if not previous_rating:
        total_ratings += 1

    if total_ratings > 0:
        average_rating = (book.average_rating * book.rating_counts) - (previous_rating.book_rating if previous_rating else 0)
        average_rating = (average_rating + int(instance.book_rating)) / total_ratings
    else:
        average_rating = instance.rating

    Book.objects.filter(pk=book.pk).update(average_rating=average_rating, rating_counts=total_ratings)
