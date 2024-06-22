# Проект api_yamdb
# **Описание**
Проект YaMDb собирает отзывы пользователей на произведения.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории: 
 - «Книги»,
 - «Фильмы»,
 - «Музыка».
# **Технологический стек**
 - Python
 - Django
 - Rest-framework
# **Как запустить проект**
 **Клонировать репозиторий и перейти в него в командной строке:**
```
git clone https://github.com/SergeyZasimov7/api_yamdb   
```
```
cd api_yamdb
```
 **Cоздать и активировать виртуальное окружение:**
```
python -m venv venv
```
```
source venv/Scripts/activate
```
 **Обновить PIP:**
```
python -m pip install --upgrade pip
```
 **Установить зависимости из файла requirements.txt:**
```
pip install -r requirements.txt
```
 **Выполнить миграции:**
```
python manage.py migrate
```
## **Добавление данных из файлов csv**
Находясь в директории с файлом manage.py прописать команду:
```
python manage.py import_csv
```
 **Запустить проект:**
```
python manage.py runserver
```
**Документация:**
```
[redoc](http://127.0.0.1:8000/redoc/) 
```
После запуска проекта, по _адресу_ будет доступна документация для проекта. В документации описано, как работает API. Документация представлена в формате Redoc.
# **Авторы:**
 - [Сергей Засимов](https://vk.com/idsfdsa) работал над: системой регистрации и аутентификации, правами доступа, работой с токеном, системой подтверждения через e-mail.
 - [Дмитрий Алеханов](https://vk.com/id146149068) работал над: произведеними, категорими, жанрами, реализацией импорта данных из csv файлов.
 - _Дмитрий Панин_ ([https://app.pachca.com/chats/9858315?user_id=316365](https://app.pachca.com/chats/9858315?user_id=316365) - manchpanch) работал над: отзывами, комментариями, рейтингами произведений.
