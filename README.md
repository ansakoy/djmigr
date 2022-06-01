# Проект для экспериментов с джанго-миграциями без привлечения внимания санитаров

### A project for experimenting with django migrations with minimal turbulence

```bash
cd djmigr

python3.9 -m venv djmigrvenv

djmigrvenv/bin/pip install --upgrade pip
djmigrvenv/bin/pip -r requirements.txt
```

```sql
create user djmigr with password 'djmigr';
CREATE DATABASE djmigr LC_COLLATE 'ru_RU.UTF-8' lc_ctype 'ru_RU.UTF-8' OWNER djmigr template template0;
```

## События
```bash
# Удаляем папки с миграциями
% rm -rf library/migrations/
```
```sql
-- Убиваем информацию о миграциях из БД
delete from django_migrations;
```
```bash
% python manage.py makemigrations
No changes detected

# Но:
% python manage.py makemigrations library
Migrations for 'library':
  library/migrations/0001_initial.py
    - Create model Author
    - Create model Book
```
Итого у нас есть база, в которой уже есть схема и данные, но после удаления старых миграций и создания 
новых у нас новые попытки смигрировать заканчиваются плохо:
```bash
% python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, library, sessions
Running migrations:
  Applying contenttypes.0001_initial...Traceback (most recent call last):
  File "/Users/ansakoy/Documents/Cheatsheets/djmigr/djmigrvenv/lib/python3.9/site-packages/django/db/backends/utils.py", line 87, in _execute
    return self.cursor.execute(sql)
psycopg2.errors.DuplicateTable: relation "django_content_type" already exists
...
```
Применяем фейк
```bash
% python manage.py migrate --fake
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, library, sessions
Running migrations:
  Applying contenttypes.0001_initial... FAKED
  Applying auth.0001_initial... FAKED
  Applying admin.0001_initial... FAKED
  Applying admin.0002_logentry_remove_auto_add... FAKED
  Applying admin.0003_logentry_add_action_flag_choices... FAKED
  Applying contenttypes.0002_remove_content_type_name... FAKED
  Applying auth.0002_alter_permission_name_max_length... FAKED
  Applying auth.0003_alter_user_email_max_length... FAKED
  Applying auth.0004_alter_user_username_opts... FAKED
  Applying auth.0005_alter_user_last_login_null... FAKED
  Applying auth.0006_require_contenttypes_0002... FAKED
  Applying auth.0007_alter_validators_add_error_messages... FAKED
  Applying auth.0008_alter_user_username_max_length... FAKED
  Applying auth.0009_alter_user_last_name_max_length... FAKED
  Applying auth.0010_alter_group_name_max_length... FAKED
  Applying auth.0011_update_proxy_permissions... FAKED
  Applying auth.0012_alter_user_first_name_max_length... FAKED
  Applying library.0001_initial... FAKED
  Applying sessions.0001_initial... FAKED
```
При следующем запуске `migrate` уже без фейка всё хорошо:
```bash
% python manage.py migrate       
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, library, sessions
Running migrations:
  No migrations to apply.
```
Действительно, никаких изменений не было. Добавим изменения:
```bash
% python manage.py makemigrations
Migrations for 'library':
  library/migrations/0002_book_publish_year.py
    - Add field publish_year to book

% python manage.py migrate       
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, library, sessions
Running migrations:
  Applying library.0002_book_publish_year... OK
(djmigrvenv) ansakoy ~/Documents/Cheatsheets/djmigr/djmigr % 
```
Сработало, и все данные на месте.
