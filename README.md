## Для запуска
1. Создайте БД
2. Вписать свои параметры БД в settings.py
```commandline
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql_psycopg2',
           'NAME': '<database_name>',
           'USER': '<database_user>',
           'PASSWORD': '<password>',
           'HOST': '<host>',
           'PORT': '5432',
   }}
   ```
3. Запустить миграцию ``python manage.py migrate``
4. Загрузить тестовые данные ``python manage.py loaddata data.json``
### Аккаунт панели администратора 
* Логин: admin
* Пароль: admin