import random

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from mainapp.models import Book


class ExploreBooksSeleniumTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Chrome()

        cls.random_books = []
        for i in range(10):
            book = Book.objects.create(
                title=f"Random Book {i}",
                authors=f"Author {i}",
                average_rating=random.uniform(1, 5),
                rating_counts=random.randint(1, 100),
                description=f"Description for Random Book {i}",
            )
            cls.random_books.append(book)

        # Создаем одну книгу с подходящими атрибутами для теста
        cls.test_book = Book.objects.create(
            title="Track of the Cat",
            authors="Tom",
            average_rating=4.5,
            rating_counts=50,
            description="A mysterious book about cats.",
        )

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_explore_books_with_selenium(self):
        # Логин пользователя
        self.browser.get(self.live_server_url + '/accounts/login/')
        username_input = self.browser.find_element(By.NAME, "login")
        password_input = self.browser.find_element(By.NAME, "password")
        username_input.send_keys("your_username")
        password_input.send_keys("your_password")
        password_input.send_keys(Keys.ENTER)

        # Открыть страницу explore
        self.browser.get(self.live_server_url + '/explore_books/')

        # Ввести "Cat" в поле поиска
        search_input = self.browser.find_element(By.ID, "search")
        search_input.send_keys("Cat")

        # Ввести "Tom" в поле автора
        author_input = self.browser.find_element(By.ID, "author")
        author_input.send_keys("Tom")

        # Выбрать жанр "mystery"
        genre_select = self.browser.find_element(By.NAME, "mystery")
        genre_select.click()

        # Выбрать сортировку "По количеству оцениваний"
        sort_select = Select(self.browser.find_element(By.ID, "sort"))
        sort_select.select_by_value("number_of_ratings")

        # Дождаться, пока обновится список книг
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "large-screen"))
        )

        # Проверить, что "Track of the Cat" присутствует в списке книг
        track_of_the_cat_element = self.browser.find_element(By.CSS_SELECTOR, '[data-book-id="1"]')
        self.assertIsNotNone(track_of_the_cat_element)
