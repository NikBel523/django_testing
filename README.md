# Django testing  
## Задача

Сформировать тесты для проверки логики, маршрутов и контента для двух готовых Django приложений.

YaNews — новостной сайт, где пользователи могут оставлять комментарии к новостям.

YaNote — электронная записная книжка для тех, кто не хочет ничего забыть и поэтому всё записывает.

Расположение тестов в проекте:

```
django_testing
   ├── ya_news
   │   ├── news
   │   │   ├── fixtures/
   │   │   ├── migrations/
   │   │   ├── pytest_tests/   <- Директория с тестами pytest для проекта ya_news
   │   │   ├── __init__.py
   │   │   ├── admin.py
   │   │   ├── apps.py
   │   │   ├── forms.py
   │   │   ├── models.py
   │   │   ├── urls.py
   │   │   └── views.py
   │   ├── templates/
   │   ├── yanews/
   │   ├── manage.py
   │   └── pytest.ini
   ├── ya_note
   │   ├── notes
   │   │   ├── migrations/
   │   │   ├── tests/          <- Директория с тестами unittest для проекта ya_note
   │   │   ├── __init__.py
   │   │   ├── admin.py
   │   │   ├── apps.py
   │   │   ├── forms.py
   │   │   ├── models.py
   │   │   ├── urls.py
   │   │   └── views.py
   │   ├── templates/
   │   ├── yanote/
   │   ├── manage.py
   │   └── pytest.ini
   ├── .gitignore
   ├── README.md
   ├── requirements.txt
   └── structure_test.py
```

## Запуск проектов

Для ознакомления с сайтами, YaNews и YaNote нужно запустить локально. 

Для этого необходимо:

1. Клонировать репозиторий ```git clone git@github.com:NikBel523/django_testing.git```

2. Создать и активировать виртуальное окружение

    ```python3 -m venv venv```

    Windows: ```source venv/Scripts/activate```

    Linux: ```source env/bin/activate```

3. Установить зависимости ```pip install -r requirements.txt```

4. Перейти в корень нужного проекта ```cd ya_news``` или ```cd ya_note```.

5. Накатить миграции ```python manage.py migrate```

6. Запустить проект ```python manage.py runserver```

## Запуск тестов

### YaNews
1. Перейти в директорию ya_news ```cd ya_news```
2. Запуск pytest ```pytest```

### YaNote
1. Перейти в директорию ya_note ```cd ya_note```
2. Запуск unittest для Django ```python manage.py test```

<br>

Стек технологий: Python, Django, pytest, unittest 

Автор: [Беляков Никита](https://github.com/NikBel523)
