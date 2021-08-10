# Yatter.

## Описание.
Учебный проект.
Социальная сеть для публикации личных дневников. Это сайт, на котором можно создать свою страницу. Если на нее зайти, то можно посмотреть все записи автора. Пользователи могут заходить на чужие страницы, подписываться на других авторов и комментировать их записи. Автор может выбрать имя и уникальный адрес для своей страницы. Записи можно отправить в группу и посмотреть в ней записи разных авторов.

### API.
Предусмотрена возможность работы с сервисом через API.
Доступ осуществляется по JWT токену. Имеется возможность: получать, создавать, изменять, удалять публикации; получать, создавать, изменять, удалять комментарии к публикациям; создать новую группу, получить список всех групп; подписаться на пользователя и отменить подписку.
Более подробная информация по работе с API доступна на странице 'redoc/'.

## Установка и запуск.
Для локального запуска установить зависимости:
```
pip install requirements.txt
```
Создать миграции:
```
py manage.py makemigrations
```
Применить миграции:
```
py manage.py migrate
```
Запустить Django development server (сайт будет доступен по адресу localhost:8000):
```
python manage.py runserver
```
