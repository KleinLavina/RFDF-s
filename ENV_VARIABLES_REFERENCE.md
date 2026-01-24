# Environment Variables Reference

Complete reference for all environment variables used in the RDFS application.

---

## Core Django Settings

### ENVIRONMENT
- **Type:** String
- **Options:** `development`, `production`
- **Default:** `development`
- **Description:** Determines the application environment. When set to `production`, enables security features.
- **Example:** `ENVIRONMENT=production`

### SECRET_KEY
- **Type:** String
- **Required:** Yes
- **Description:** Django secret key for cryptographic signing. Must be unique and kept secret.
- **Generate:** `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
- **Example:** `SECRET_KEY=django-insecure-abc123...`

### DEBUG
- **Type:** Boolean
- **Default:** `False`
- **Description:** Enable/disable debug mode. Must be `False` in production.
- **Example:** `DEBUG=False`

### ALLOWED_HOSTS
- **Type:** Comma-separated list
- **Default:** `127.0.0.1,localhost`
- **Description:** List of host/domain names that Django can serve.
- **Example:** `ALLOWED_HOSTS=rfdf-s.onrender.com,www.example.com`

---

## Database Configuration

### DATABASE_URL
- **Type:** PostgreSQL connection URL
- **Required:** Yes
- **Format:** `postgresql://username:password@host:port/database_name`
- **Description:** Complete PostgreSQL database connection string.
- **Examples:**
  - Local: `postgresql://postgres:admin@localhost:5432/rdfs_db`
  - Render Internal: `postgresql://rdfs_database_user:5f4yOSRpmltsamQvKYLbWwfuJbroy90A@dpg-d5q3366r433s73fovhb0-a/rdfs_database`
  - Neon: `postgresql://user:pass@host.neon.tech/db?sslmode=require`

---

## Media Storage (Cloudinary)

### CLOUDINARY_URL
- **Type:** Cloudinary connection URL
- **Required:** Yes (if using Cloudinary)
- **Format:** `cloudinary://api_key:api_secret@cloud_name`
- **Description:** Complete Cloudinary credentials in URL format.
- **Example:** `CLOUDINARY_URL=cloudinary://123456:abcdef@mycloud`

### Alternative: Individual Cloudinary Variables

If not using `CLOUDINARY_URL`, you can use these instead:

#### CLOUDINARY_CLOUD_NAME
- **Type:** String
- **Description:** Your Cloudinary cloud name

#### CLOUDINARY_API_KEY
- **Type:** String
- **Description:** Your Cloudinary API key

#### CLOUDINARY_API_SECRET
- **Type:** String
- **Description:** Your Cloudinary API secret

---

## Redis Configuration (Optional)

### USE_REDIS_CHANNEL_LAYER
- **Type:** Boolean
- **Default:** `False`
- **Description:** Enable Redis for Django Channels (WebSockets). Recommended for production.
- **Example:** `USE_REDIS_CHANNEL_LAYER=True`

### REDIS_URL
- **Type:** Redis connection URL
- **Default:** `redis://127.0.0.1:6379`
- **Description:** Redis server connection string. Only needed if `USE_REDIS_CHANNEL_LAYER=True`.
- **Examples:**
  - Local: `redis://127.0.0.1:6379`
  - Render: `redis://red-xxxxx:6379`
  - With password: `redis://:password@host:6379`

---

## Django Superuser (Auto-creation)

### DJANGO_SUPERUSER_USERNAME
- **Type:** String
- **Default:** None
- **Description:** Username for auto-created superuser.
- **Example:** `DJANGO_SUPERUSER_USERNAME=adminterminal`

### DJANGO_SUPERUSER_EMAIL
- **Type:** Email
- **Default:** None
- **Description:** Email for auto-created superuser.
- **Example:** `DJANGO_SUPERUSER_EMAIL=admin@example.com`

### DJANGO_SUPERUSER_PASSWORD
- **Type:** String
- **Default:** None
- **Description:** Password for auto-created superuser. Use strong password in production.
- **Example:** `DJANGO_SUPERUSER_PASSWORD=SecurePass123!`

---

## Session Configuration

### SESSION_COOKIE_AGE
- **Type:** Integer (seconds)
- **Default:** `900` (15 minutes)
- **Description:** Session timeout duration in seconds.
- **Examples:**
  - 15 minutes: `SESSION_COOKIE_AGE=900`
  - 30 minutes: `SESSION_COOKIE_AGE=1800`
  - 1 hour: `SESSION_COOKIE_AGE=3600`

### SESSION_COOKIE_SECURE
- **Type:** Boolean
- **Default:** `True` (in production), `False` (in development)
- **Description:** Whether to use secure cookies (HTTPS only).
- **Example:** `SESSION_COOKIE_SECURE=True`

### CSRF_COOKIE_SECURE
- **Type:** Boolean
- **Default:** `True` (in production), `False` (in development)
- **Description:** Whether to use secure CSRF cookies (HTTPS only).
- **Example:** `CSRF_COOKIE_SECURE=True`

---

## Security Settings (Production)

These are automatically enabled when `ENVIRONMENT=production`, but can be overridden:

### SECURE_SSL_REDIRECT
- **Type:** Boolean
- **Default:** `True` (in production)
- **Description:** Redirect all HTTP requests to HTTPS.
- **Example:** `SECURE_SSL_REDIRECT=True`

### SECURE_HSTS_SECONDS
- **Type:** Integer (seconds)
- **Default:** `31536000` (1 year)
- **Description:** HTTP Strict Transport Security duration.
- **Example:** `SECURE_HSTS_SECONDS=31536000`

### SECURE_HSTS_INCLUDE_SUBDOMAINS
- **Type:** Boolean
- **Default:** `True` (in production)
- **Description:** Include subdomains in HSTS policy.
- **Example:** `SECURE_HSTS_INCLUDE_SUBDOMAINS=True`

### SECURE_HSTS_PRELOAD
- **Type:** Boolean
- **Default:** `True` (in production)
- **Description:** Enable HSTS preload.
- **Example:** `SECURE_HSTS_PRELOAD=True`

---

## Deployment-Specific

### PYTHON_VERSION
- **Type:** String
- **Default:** Specified in `runtime.txt`
- **Description:** Python version for deployment (Render).
- **Example:** `PYTHON_VERSION=3.11.7`

---

## Environment Variable Priority

1. **System environment variables** (highest priority)
2. **.env file** (local development)
3. **Default values in settings.py** (lowest priority)

---

## Security Best Practices

1. **Never commit `.env` file** to version control
2. **Use different SECRET_KEY** for each environment
3. **Use strong passwords** for database and superuser
4. **Enable HTTPS** in production (`SECURE_SSL_REDIRECT=True`)
5. **Set DEBUG=False** in production
6. **Restrict ALLOWED_HOSTS** to your actual domains
7. **Use environment-specific credentials** (don't reuse dev credentials in production)

---

## Quick Setup Checklist

### Local Development
- [ ] Copy `.env.example` to `.env`
- [ ] Set `ENVIRONMENT=development`
- [ ] Set `DEBUG=True`
- [ ] Configure local `DATABASE_URL`
- [ ] Set Cloudinary credentials
- [ ] Generate `SECRET_KEY`

### Production (Render)
- [ ] Set `ENVIRONMENT=production`
- [ ] Set `DEBUG=False`
- [ ] Generate new `SECRET_KEY`
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Configure production `DATABASE_URL` (use Internal URL)
- [ ] Set Cloudinary credentials
- [ ] Set strong superuser password
- [ ] Verify all security settings

---

## Troubleshooting

### Database Connection Issues
- Verify `DATABASE_URL` format is correct
- Check database server is running
- Ensure credentials are correct
- For Render, use Internal Database URL for better performance

### Static Files Not Loading
- Run `python manage.py collectstatic`
- Check `STATIC_ROOT` and `STATIC_URL` settings
- Verify WhiteNoise is installed

### Media Upload Issues
- Verify `CLOUDINARY_URL` is correct
- Check Cloudinary dashboard for errors
- Ensure API credentials have proper permissions

### Session/Cookie Issues
- Check `SESSION_COOKIE_SECURE` matches your HTTPS setup
- Verify `CSRF_COOKIE_SECURE` settings
- Clear browser cookies and try again

---

## Additional Resources

- [Django Settings Documentation](https://docs.djangoproject.com/en/5.0/ref/settings/)
- [django-environ Documentation](https://django-environ.readthedocs.io/)
- [Render Documentation](https://render.com/docs)
- [Cloudinary Documentation](https://cloudinary.com/documentation)
