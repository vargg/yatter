# Yatter.

## Стэк
[Python](https://www.python.org/) v.3.8.5, [Django](https://www.djangoproject.com/) v.2.2.6, [Django REST framework](https://www.django-rest-framework.org/) v.3.12.4, [DRF simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) v.4.6.0, [PostgreSQL](https://www.postgresql.org) v.12.4, [Nginx](https://nginx.org/en/docs/) v.1.19.3, [Docker](https://www.docker.com/) v.20.10.8.

## Описание.
Социальная сеть для публикации личных дневников. Это сайт, на котором можно создать свою страницу. Если на нее зайти, то можно посмотреть все записи автора. Пользователи могут заходить на чужие страницы, подписываться на других авторов и комментировать их записи. Автор может выбрать имя и уникальный адрес для своей страницы. Записи можно отправить в группу и посмотреть в ней записи разных авторов.

### API.
Предусмотрена возможность работы с сервисом через API.
Доступ осуществляется по JWT токену. Имеется возможность: получать, создавать, изменять, удалять публикации; получать, создавать, изменять, удалять комментарии к публикациям; создать новую группу, получить список всех групп; подписаться на пользователя и отменить подписку.
Более подробная информация по работе с API доступна на странице 'redoc/'.

## Установка и запуск.
Для запуска требуются [docker](https://docs.docker.com/get-docker/) и [docker compose](https://docs.docker.com/compose/install/).
Клонировать репозиторий:
```shell
git clone https://github.com/vargg/yamdb_final.git
```
В корневом каталоге проекта создать файл `.env` в котором должны быть заданы следующие переменные:
```
-DB_NAME
-DB_ENGINE
-DB_USER
-DB_PASSWORD
-POSTGRES_PASSWORD
-DB_HOST
-DB_PORT
-DEBUG
-DJANGO_SECRET_KEY
```
Запуск контейнеров:
```shell
docker-compose up
```
Сервис будет доступен по ссылке [http://localhost](http://localhost).

Применение миграций:
```shell
docker-compose exec -T web python manage.py migrate
```
Для сбора статики:
```shell
docker-compose exec -T web python manage.py collectstatic --no-input
```
Остановка:
```shell
docker-compose down
```
