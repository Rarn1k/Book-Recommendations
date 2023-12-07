from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Genre, Book, UserRating, SaveForLater


class BaseTestCase(TestCase):
    def setUp(self):

        # Создаем несколько жанров
        self.fiction_genre = Genre.objects.create(name='fiction')
        self.mystery_genre = Genre.objects.create(name='mystery')
        self.romance_genre = Genre.objects.create(name='romance')

        # Создаем 20 книг, присваивая им жанры
        for i in range(1, 21):
            book = Book.objects.create(
                title=f'Book {i}',
                authors=f'Author {i}',
                average_rating=4.0,
                rating_counts=50 + i,
                description=f'Description {i}'
            )
            if i % 2 == 0:
                book.genre.set([self.fiction_genre, self.mystery_genre])
            else:
                book.genre.set([self.romance_genre])

        # Создаем пользователя и оценки книг
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        for i in range(1, 11):
            book = Book.objects.get(title=f'Book {i}')
            UserRating.objects.create(user=self.user, book=book, book_rating=5)


class ExploreBooksViewTest(BaseTestCase):

    def test_explore_books_view(self):
        url = reverse('explore_books')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        # Проверяем, что в ответе есть книги из базы данных
        self.assertContains(response, 'Book 1')
        self.assertContains(response, 'Book 2')


class PersonalRecommendationsViewTest(BaseTestCase):

    def test_personal_recommendations_view(self):
        # Авторизуем пользователя
        self.client.login(username='testuser', password='testpassword')

        # Формируем URL для вьюхи personal_recommendations
        url = reverse('personal_recommendations')

        # Отправляем GET-запрос на URL
        response = self.client.get(url)

        # Проверяем, что запрос возвращает успешный статус (200)
        self.assertEqual(response.status_code, 200)


class SavedListViewTest(BaseTestCase):

    def test_saved_list_view_with_books(self):
        # Авторизуем пользователя
        self.client.login(username='testuser', password='testpassword')

        # Создаем книгу для тестирования
        book = Book.objects.create(
            title='Test Book for Saved List',
            authors='Test Author',
            average_rating=4.0,
            rating_counts=60,
            description='Test Description'
        )

        # Сохраняем книгу для пользователя
        SaveForLater.objects.create(user=self.user, book=book)

        # Формируем URL для вьюхи saved_list
        url = reverse('saved_list')

        # Отправляем GET-запрос на URL
        response = self.client.get(url)

        # Проверяем, что запрос возвращает успешный статус (200)
        self.assertEqual(response.status_code, 200)

        # Проверяем, что в ответе присутствует ожидаемый контент
        self.assertContains(response, 'Test Book for Saved List')

    def test_saved_list_view_no_books(self):
        # Авторизуем пользователя
        self.client.login(username='testuser', password='testpassword')

        # Формируем URL для вьюхи saved_list
        url = reverse('saved_list')

        # Отправляем GET-запрос на URL
        response = self.client.get(url, follow=True)  # Устанавливаем follow=True для обработки перенаправлений

        # Проверяем, что запрос вызывает перенаправление
        self.assertRedirects(response, reverse('index'))

        # Получаем сообщения
        messages = list(get_messages(response.wsgi_request))

        # Проверяем, что в сообщениях есть информация о том, что нет сохраненных книг
        self.assertIn('У вас нет сохраненных книг', [str(message) for message in messages])


class RatedBooksViewTest(BaseTestCase):

    def test_rated_books_view_with_ratings(self):
        # Авторизуем пользователя
        self.client.login(username='testuser', password='testpassword')

        # Формируем URL для вьюхи rated_books
        url = reverse('rated_books')

        # Отправляем GET-запрос на URL
        response = self.client.get(url)

        # Проверяем, что запрос возвращает успешный статус (200)
        self.assertEqual(response.status_code, 200)

        # Проверяем, что в ответе присутствует ожидаемый контент
        for i in range(1, 11):
            self.assertContains(response, f'Book {i}')

    def test_rated_books_view_without_ratings(self):
        # Авторизуем пользователя
        self.client.login(username='testuser', password='testpassword')

        # Удаляем оценки у пользователя
        UserRating.objects.filter(user=self.user).delete()

        # Формируем URL для вьюхи rated_books
        url = reverse('rated_books')

        # Отправляем GET-запрос на URL
        response = self.client.get(url)

        # Проверяем, что запрос вызывает перенаправление (302)
        self.assertEqual(response.status_code, 302)

        # Проверяем, что перенаправление идет на ожидаемый URL (в данном случае, на страницу входа)
        self.assertRedirects(response, reverse('index'))

        # Получаем сообщения
        messages = list(get_messages(response.wsgi_request))

        # Проверяем, что в сообщениях есть информация о том, что нет сохраненных книг
        self.assertIn('У вас нет оцененных книг', [str(message) for message in messages])