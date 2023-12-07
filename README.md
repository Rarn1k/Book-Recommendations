# Book-Recommendations
## Рекомендательная система книг


### Цель проекта: 
- разработка приложения, предоставляющее пользователям рекоммендации книг для прочтения.


### Задачи:
1. Хранение информации о книгах
2. Фильтрация и сортировка книг по жанрам, авторам, году выпуска, рейтингу
3. Возможность пользователям оставлять отзывы и оценки книгам
4. Уведомления: пользователи могут подписаться на уведомления о новых книгах в выбранном жанре
5. Рекомендации на основе коллаборативной фильтрации: система может анализировать общие предпочтения пользователей и предлагать им книги, оцененные или прочитанные другими пользователями с похожими вкусами

### Стек технологий:

- Django

- PostgreSQL

### Разработанный функционал и используемые методы
В данном приложении пользователи могут видеть топ популярных книг среди пользователей системы. Имеется возможность смотреть краткое описание книги, авторов и средний рейтинг.
Топ популярных книг расчитывается по формуле рейтинга IMDb:

Средневзвешенный рейтинг = (v ÷ (v+m)) × R + (m ÷ (v+m)) × C

R = средний рейтинг

v = число голосов за книгу

m = минимум голосов для участия в списке

C = среднее значение всего рейтинга

Пользователь может искать книги по определенному жанру, названию или автору. Также есть возможность сортировать результаты поиска по различным критериям.

Авторизованный пользователь может оценивать книги и добавлять в личный список "Избранное", чтобы сохранять книги для дальнейшего прочтения. 

Для каждого пользователя система предоставляет персонализированные рекоммендации на основе предпочтений других пользователей с похожими вкусами. В качестве алгоритма используется алгоритм Коллаборативной Фильтрации типа User-Item:

1. Берется исходный пользователь.
2. Находится группа пользователей, которая максимально похожа на него (основываясь, оценках) и узнаётся, какие книги понравились этой группе.
3. Исходному пользователю рекомендуются книги, которые нравятся найденной группе пользователей.

На входе - пользователь, на выходе – рекомендация книг для данного пользователя.

В качестве метрики близости в данной работе используется косинусное расстояние между векторами пользователей.

Для создания прогноза неизвестных оценок пользователей используется библиотека surprise. В predict_model.py создается и обучается модель по данным оценок всех пользователей системы. Затем создается прогноз и сохраняется в static/mainapp/model_surprise.

### Dataset
Данные для приложения (книги и рейтинги пользователей) взяты из [goodbooks-10k](https://github.com/zygmuntz/goodbooks-10k). Для заполнения базы данных приложения из csv файлов необходимо запустить parser.py


### Архитектура приложения:
```
Book-Recommendations
|-- mainapp              
|   |-- migrations       #миграции
|   |-- templates        #шаблоны приложения
|   |-- handling.py      #обработка данных для представлений
|   |-- models.py        #модели
|   |-- parser.py        #парсинг датасета в бд
|   |-- predict_model.py #обучение модели и создание рекомендаций
|   |-- tests.py         #тесты  
|   |-- urls.py          #маршруты  
|   |-- views.py         #представления 
|   |-- views_ajax.py    #представления для ajax 
|--media                 #изображения
|--root                  #главная папка проекта
|--static 
|   |--dataset
|       |--books.scv     #данные о книгах
|       |--raitings.scv  #данные об оценках пользователей
|   |--gif
|   |--mainapp
|       |--css          #css файлы
|       |--png          #изображения
|   |--model_surprise   #сериализованная модель прогнозирования 
|
```
