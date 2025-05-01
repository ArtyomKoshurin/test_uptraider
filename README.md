# Проект tree_menu
Проект для отображения древовидных меню.
Техническое задание: https://drive.google.com/drive/folders/1irsS023RO32RO4trOHMhW4rzEykMvbIt?hl=ru

# Установка и развертывание проекта на локальном сервере
1. Склонируйте репозиторий. 
2. Создайте и активируйте виртуальное окружение
```
python -m venv venv
source venv/Scripts/activate
```
3. Перейдите в директорию /tree_menu/
4. Установите зависимости из requirements.txt `pip install -r requirements.txt`
5. Создайте .env-файл со значениями SECRET_KEY, DEBUG и ALLOWED_HOSTS
6. Создайте и выполните миграции 
```
python manage.py makemigrations
python manage.py migrate
```
7. Создайте админскую учетку `python manage.py createsuperuser`
8. Запустите локальный сервер `python manage.py runserver`
9. Главная страница будет доступна по эндпоинту https://127.0.0.1:8000/
Админка - по эндпоинту https://127.0.0.1:8000/admin/

# Автор:
Кошурин Артём