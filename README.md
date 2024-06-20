# Проект api_yamdb
# **Описание**
Проект YaMDb собирает отзывы пользователей на произведения.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории: 
 - «Книги»,
 - «Фильмы»,
 - «Музыка».
### **Как запустить проект**

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/SergeyZasimov7/api_yamdb   
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Обновить PIP:

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py makemigrations
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```
Документация:
```
http://127.0.0.1:8000/redoc/
```
После запуска проекта, по _адресу_ будет доступна документация для проекта. В документации описано, как работает API. Документация представлена в формате Redoc.
