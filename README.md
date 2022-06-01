# Проект для экспериментов с джанго-миграциями без привлечения внимания санитаров

### A project for experimenting with django migrations with minimal turbulence

## Установка
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

Теперь допустим, что мы не просто удалили миграции, а внесли еще изменения в модели и теперь хотим 
это всё смигрировать в базу, не удаляя данные.

Удаляем миграции:
```bash
rm -rf library/migrations 
``` 
Создаем новые атрибуты у моделей `library`, а заодно и вообще новый апп `blog` со своими моделями.

Пробуем создать миграции:
```bash
% python manage.py makemigrations
Migrations for 'blog':
  blog/migrations/0001_initial.py
    - Create model Entry
    - Create model Comment
```
Миграции создались, но только для нового аппа. И они даже успешно применились для нового аппа:
```bash
% python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, blog, contenttypes, sessions
Running migrations:
  Applying blog.0001_initial... OK
```
Но в старом аппе миграции закономерным образом не появились. Создадим прицельно:
```bash
% python manage.py makemigrations library
Migrations for 'library':
  library/migrations/0001_initial.py
    - Create model Author
    - Create model Book
```
Смигрироваться, конечно, не смигрируется, потому что в базе уже отмечена миграция 0001 как состоявшаяся:
```bash
% python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, blog, contenttypes, library, sessions
Running migrations:
  No migrations to apply.
```
Чтобы она не мешалась, удалим из базы все миграции (`delete from django_migrations;`).

И для полноты картины положим какие-нибудь данные в таблицы нового аппа.

Делаем фейковые миграции (`python manage.py makemigrations --fake`). Успешно.

Всё прекрасно, только миграции 0001 из аппа `library` (и соответственно изменения в них) теперь невидимы для джанго. 
Посмотрим, что получится, если вбросить какое-нибудь еще изменение и попробовать его смигрировать. 
```bash
% python manage.py makemigrations
Migrations for 'library':
  library/migrations/0002_book_useless_field.py
    - Add field useless_field to book
```
```bash
% python manage.py migrate       
Operations to perform:
  Apply all migrations: admin, auth, blog, contenttypes, library, sessions
Running migrations:
  Applying library.0002_book_useless_field... OK
```

Смигрировалось без ошибок. Но только миграцию 0001, где были дополнительные поля, по-прежнему не видим. 
В итоге в базу добавилось только новое поле из 0002, а поля, добавленные в первой сгенерированной миграции 
так и остаются за кадром, ибо такова суть фальшивых миграций.

Проблема в том, что в первой миграции есть старые поля, которые уже есть в базе, и мигрировать их не нужно, 
то есть в этой части миграцию можно правда сфальсифицировать. А есть новые поля, которых в базе еще нет. То есть 
нужна как бы разница - старое не трогать, а новые запустить по-настоящему.

Для чистоты эксперимента опять убьем миграции в аппах и в базе тоже.

Попробуем `--fake-initial`
```bash
% python manage.py migrate --fake-initial
Operations to perform:
  Apply all migrations: admin, auth, blog, contenttypes, library, sessions
Running migrations:
  Applying contenttypes.0001_initial... FAKED
  Applying auth.0001_initial... FAKED
  Applying admin.0001_initial... FAKED
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name...Traceback (most recent call last):
  File "/Users/ansakoy/Documents/Cheatsheets/djmigr/djmigrvenv/lib/python3.9/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
psycopg2.errors.UndefinedColumn: column "name" of relation "django_content_type" does not exist
```
Упс. Ладно, попробуем частями. Откатимся к исходной позиции: в наших аппах нет миграций, в базе сведения о миграциях 
удалены. Сначала сфальсифицируем существующие миграции встроенных джанго-приложений:
```bash
% python manage.py migrate --fake
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
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
  Applying sessions.0001_initial... FAKED
```
Допустим. Теперь сгенерируем миграции наших приложений и попробуем таки сделать `--fake-initial`. 
Сделалось, но собственно это привело к фальсификации этих самых единственных файлов с миграциями, которые 
образовались по итогам перегенерации.

Мораль:  
* `migrate --fake` нужно для того, чтобы "проматывать" миграции к нужному состоянию, подгодняя их под те 
изменения, которые были внесены в схему базы руками. То есть создали в базе новую таблиц или добавили поле, 
записали это в моделях, прогнали фейк. Теперь в базе в django_migrations отмечено, что эта миграция 
уже применена, и не будет скандалов, что, мол такая таблица/поле уже есть в базе.
* `migrate --fake-initial` нужно для того, чтобы решать проблему сосуществования первой миграции, полностью 
соответствующей уже существующей схеме базы, и всех последующих, которые должны изменить эту схему. Если 
запустить миграции с этой опцией, опять же, для начальной миграции будет сгенерирована запись в базе, что дескать 
она уже применена, а последующие уже применятся по-настоящему.

Ни то, ни другое не решает проблему с "дельтой", когда в одной миграции (по совпадению начальной) 
у нас есть и старое, и новое.

Такое впечатление, что придется таки лезть в миграции руками и разводить старое и новое