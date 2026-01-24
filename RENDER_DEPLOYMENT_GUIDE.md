# RDFS - Render Deployment Guide

## Overview
This guide covers deploying the RDFS application to Render with PostgreSQL database.

---

## 1. Environment Variables for Render

### Required Environment Variables

Set these in your Render Web Service dashboard under **Environment**:

```bash
# Core Django Settings
ENVIRONMENT=production
SECRET_KEY=<generate-new-secret-key>
DEBUG=False
PYTHON_VERSION=3.11.7

# Allowed Hosts
ALLOWED_HOSTS=rfdf-s.onrender.com

# Database (Use Internal Database URL for better performance)
DATABASE_URL=postgresql://rdfs_database_user:5f4yOSRpmltsamQvKYLbWwfuJbroy90A@dpg-d5q3366r433s73fovhb0-a/rdfs_database

# Cloudinary Media Storage
CLOUDINARY_URL=cloudinary://815149276221998:xsaht6ViI6EfnCdtPK6hBCGqoAk@dkqrcxc59

# Django Superuser (for auto-creation)
DJANGO_SUPERUSER_USERNAME=adminterminal
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=<strong-password-here>

# Session Configuration
SESSION_COOKIE_AGE=900

# Redis (Optional - if you add Redis service)
USE_REDIS_CHANNEL_LAYER=False
# REDIS_URL=redis://red-xxxxx:6379
```

---

## 2. Generate a New SECRET_KEY

**IMPORTANT:** Never use the same SECRET_KEY in production as in development!

Generate a new one:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Copy the output and set it as your `SECRET_KEY` environment variable in Render.

---

## 3. Database Setup on Render

### Option A: Using Render PostgreSQL (Recommended)

1. **Create PostgreSQL Database:**
   - Go to Render Dashboard → New → PostgreSQL
   - Name: `rdfs_database`
   - Region: Same as your web service
   - Plan: Choose based on your needs

2. **Get Connection URLs:**
   - **Internal Database URL** (faster, use this): 
     ```
     postgresql://rdfs_database_user:5f4yOSRpmltsamQvKYLbWwfuJbroy90A@dpg-d5q3366r433s73fovhb0-a/rdfs_database
     ```
   - **External Database URL** (for external connections):
     ```
     postgresql://rdfs_database_user:5f4yOSRpmltsamQvKYLbWwfuJbroy90A@dpg-d5q3366r433s73fovhb0-pooler.oregon-postgres.render.com/rdfs_database
     ```

3. **Set DATABASE_URL:**
   - In your Render Web Service, set `DATABASE_URL` to the **Internal Database URL**

### Option B: Using External PostgreSQL (Neon, etc.)

If you prefer to use an external PostgreSQL provider:

```bash
DATABASE_URL=postgresql://neondb_owner:npg_pXJ9lYwk2EoL@ep-muddy-water-ahpqjyj0-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require
```

---

## 4. Render Web Service Configuration

### Build Command
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

### Start Command
```bash
gunicorn rdfs.wsgi:application
```

### Environment Variables Summary

| Variable | Value | Notes |
|----------|-------|-------|
| `ENVIRONMENT` | `production` | Required |
| `SECRET_KEY` | `<generated-key>` | Generate new for production |
| `DEBUG` | `False` | Must be False in production |
| `ALLOWED_HOSTS` | `rfdf-s.onrender.com` | Your Render domain |
| `DATABASE_URL` | `postgresql://...` | Use Internal URL |
| `CLOUDINARY_URL` | `cloudinary://...` | Your Cloudinary credentials |
| `DJANGO_SUPERUSER_USERNAME` | `adminterminal` | Admin username |
| `DJANGO_SUPERUSER_EMAIL` | `admin@example.com` | Admin email |
| `DJANGO_SUPERUSER_PASSWORD` | `<strong-password>` | Admin password |
| `PYTHON_VERSION` | `3.11.7` | Python version |
| `SESSION_COOKIE_AGE` | `900` | Session timeout (seconds) |

---

## 5. Database Migration Steps

### Initial Setup (First Deployment)

1. **Deploy your application** to Render
2. **Wait for build to complete**
3. **Migrations run automatically** via build command
4. **Create superuser** (if not auto-created):
   ```bash
   # In Render Shell
   python manage.py create_admin
   ```

### Switching from Old Database to New Database

If you're switching from Neon to Render PostgreSQL:

#### Option A: Fresh Start (Recommended for Development)

1. Update `DATABASE_URL` to new Render PostgreSQL URL
2. Redeploy
3. Migrations will create fresh tables
4. Superuser will be auto-created

#### Option B: Migrate Existing Data

1. **Backup old database:**
   ```bash
   pg_dump "postgresql://neondb_owner:npg_pXJ9lYwk2EoL@ep-muddy-water-ahpqjyj0-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require" > backup.sql
   ```

2. **Restore to new database:**
   ```bash
   psql "postgresql://rdfs_database_user:5f4yOSRpmltsamQvKYLbWwfuJbroy90A@dpg-d5q3366r433s73fovhb0-pooler.oregon-postgres.render.com/rdfs_database" < backup.sql
   ```

3. **Update DATABASE_URL** in Render
4. **Redeploy**

---

## 6. Post-Deployment Checklist

- [ ] Application loads without errors
- [ ] Can log in with superuser credentials
- [ ] Database connections work
- [ ] Static files load correctly
- [ ] Media uploads work (Cloudinary)
- [ ] All pages accessible
- [ ] WebSocket connections work (if using)
- [ ] Session timeout works as expected
- [ ] HTTPS redirect works
- [ ] No sensitive data in logs

---

## 7. Monitoring & Maintenance

### Check Logs
```bash
# In Render Dashboard
Logs → View Logs
```

### Common Issues

**Issue: Static files not loading**
- Solution: Check `STATIC_ROOT` and run `collectstatic`

**Issue: Database connection errors**
- Solution: Verify `DATABASE_URL` is correct (use Internal URL)

**Issue: 500 errors**
- Solution: Check logs, ensure `DEBUG=False` and `ALLOWED_HOSTS` is set

**Issue: Media uploads fail**
- Solution: Verify `CLOUDINARY_URL` is correct

---

## 8. Security Best Practices

1. **Never commit `.env` file** - Already in `.gitignore`
2. **Use strong SECRET_KEY** - Generate new for production
3. **Use strong passwords** - For superuser and database
4. **Enable HTTPS** - Automatic on Render
5. **Regular backups** - Backup database regularly
6. **Monitor logs** - Check for suspicious activity
7. **Update dependencies** - Keep packages up to date

---

## 9. Scaling Considerations

### Database
- Start with Render PostgreSQL Starter plan
- Upgrade as needed based on usage
- Consider connection pooling for high traffic

### Web Service
- Start with Starter plan
- Monitor CPU/Memory usage
- Scale up if needed

### Redis (Optional)
- Add Redis service for WebSocket scaling
- Set `USE_REDIS_CHANNEL_LAYER=True`
- Update `REDIS_URL` with Render Redis URL

---

## 10. Rollback Plan

If deployment fails:

1. **Revert to previous deployment** in Render Dashboard
2. **Check logs** for errors
3. **Fix issues** locally
4. **Test thoroughly** before redeploying
5. **Restore database backup** if needed

---

## Support

For issues:
1. Check Render logs
2. Review Django error messages
3. Verify environment variables
4. Test database connection
5. Check Cloudinary configuration

---

## Quick Reference

### Generate SECRET_KEY
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Run Migrations
```bash
python manage.py migrate
```

### Create Superuser
```bash
python manage.py create_admin
```

### Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Test Database Connection
```bash
python manage.py dbshell
```
