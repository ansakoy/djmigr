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
```
# Удаляем папки с миграциями
% rm -rf library/migrations/

% python manage.py makemigrations
No changes detected

# Но:
% python manage.py makemigrations library
Migrations for 'library':
  library/migrations/0001_initial.py
    - Create model Author
    - Create model Book
```
```
python manage.py migrate --fake
```

```sql
-- Убиваем информацию о миграциях из БД
delete from django_migrations;
```
