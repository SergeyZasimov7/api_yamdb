# Проект api_yamdb
# **Описание**
Проект YaMDb собирает отзывы пользователей на произведения.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории: 
 - «Книги»,
 - «Фильмы»,
 - «Музыка».
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
 **Запустить проект:**
```
python manage.py runserver
```
Документация:
```
[http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/) 
```
После запуска проекта, по _адресу_ будет доступна документация для проекта. В документации описано, как работает API. Документация представлена в формате Redoc.
# **Авторы:**
 - _Сергей Засимов_ ([https://app.pachca.com/chats/7630890?user_id=316325](https://app.pachca.com/chats/7630890?user_id=316325) - zasimovsergey) работал над: системой регистрации и аутентификации, правами доступа, работой с токеном, системой подтверждения через e-mail.
 - _Дмитрий Алеханов_ ([https://app.pachca.com/chats/9853081?user_id=316307](https://app.pachca.com/chats/9853081?user_id=316307) - Дмитрий_Алеханов) работал над: произведеними, категорими, жанрами, реализацией импорта данных из csv файлов.
 - _Дмитрий Панин_ ([https://app.pachca.com/chats/9858315?user_id=316365](https://app.pachca.com/chats/9858315?user_id=316365) - manchpanch) работал над: отзывами, комментариями, рейтингами произведений.
