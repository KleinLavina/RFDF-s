# Quick Reference Card

## Essential Commands

### Generate SECRET_KEY
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Local Setup
```bash
# Linux/Mac
./setup_local.sh

# Windows
setup_local.bat
```

### Run Development Server
```bash
python manage.py runserver
```

### Database Commands
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py create_admin

# Database shell
python manage.py dbshell

# Check migrations
python manage.py showmigrations
```

### Static Files
```bash
python manage.py collectstatic --noinput
```

---

## Environment Variables (Render)

```bash
ENVIRONMENT=production
SECRET_KEY=<generate-new>
DEBUG=False
ALLOWED_HOSTS=rfdf-s.onrender.com
DATABASE_URL=postgresql://rdfs_database_user:5f4yOSRpmltsamQvKYLbWwfuJbroy90A@dpg-d5q3366r433s73fovhb0-a/rdfs_database
CLOUDINARY_URL=cloudinary://815149276221998:xsaht6ViI6EfnCdtPK6hBCGqoAk@dkqrcxc59
DJANGO_SUPERUSER_USERNAME=adminterminal
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=<strong-password>
SESSION_COOKIE_AGE=900
USE_REDIS_CHANNEL_LAYER=False
PYTHON_VERSION=3.11.7
```

---

## Database URLs

### Local
```
postgresql://postgres:admin@localhost:5432/rdfs_db
```

### Render (Internal - Use This)
```
postgresql://rdfs_database_user:5f4yOSRpmltsamQvKYLbWwfuJbroy90A@dpg-d5q3366r433s73fovhb0-a/rdfs_database
```

### Render (External - For Backups)
```
postgresql://rdfs_database_user:5f4yOSRpmltsamQvKYLbWwfuJbroy90A@dpg-d5q3366r433s73fovhb0-pooler.oregon-postgres.render.com/rdfs_database
```

---

## Render Build/Start Commands

### Build Command
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

### Start Command
```bash
gunicorn rdfs.wsgi:application
```

---

## Database Backup/Restore

### Backup
```bash
pg_dump "DATABASE_URL" > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restore
```bash
psql "DATABASE_URL" < backup_YYYYMMDD_HHMMSS.sql
```

---

## Troubleshooting

### Check Logs (Render)
Dashboard → Logs → View Logs

### Test Database Connection
```bash
python manage.py dbshell
```

### Clear Database (Careful!)
```bash
psql "DATABASE_URL" -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
```

### Check Environment Variables
```bash
python manage.py shell
>>> from django.conf import settings
>>> print(settings.DEBUG)
>>> print(settings.DATABASES)
```

---

## Documentation Files

- `DEPLOYMENT_SUMMARY.md` - Overview and quick start
- `RENDER_DEPLOYMENT_GUIDE.md` - Complete deployment guide
- `ENV_VARIABLES_REFERENCE.md` - All environment variables
- `DATABASE_MIGRATION_CHECKLIST.md` - Migration steps
- `.env.example` - Environment template

---

## Security Checklist

- [ ] New SECRET_KEY for production
- [ ] DEBUG=False in production
- [ ] Strong superuser password
- [ ] ALLOWED_HOSTS set correctly
- [ ] .env not in git
- [ ] HTTPS enabled
- [ ] Database credentials secure

---

## Support Resources

- Django Docs: https://docs.djangoproject.com/
- Render Docs: https://render.com/docs
- django-environ: https://django-environ.readthedocs.io/
- Cloudinary: https://cloudinary.com/documentation
