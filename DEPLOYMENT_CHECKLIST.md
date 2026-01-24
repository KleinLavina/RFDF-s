# Deployment Checklist

Use this checklist to ensure a smooth deployment to Render.

---

## Pre-Deployment

### Local Testing
- [ ] Application runs locally without errors
- [ ] All features tested and working
- [ ] Database migrations applied
- [ ] Static files collected
- [ ] Environment variables configured in `.env`
- [ ] No hardcoded credentials in code
- [ ] `.env` file not committed to git

### Code Review
- [ ] All changes committed to git
- [ ] No sensitive data in repository
- [ ] Requirements.txt up to date
- [ ] Runtime.txt specifies Python 3.11.7
- [ ] Settings.py uses environment variables
- [ ] No DEBUG=True in production code

---

## Render Setup

### 1. Create PostgreSQL Database
- [ ] Go to Render Dashboard → New → PostgreSQL
- [ ] Name: `rdfs_database`
- [ ] Region: Same as web service
- [ ] Plan: Starter or higher
- [ ] Note down Internal Database URL
- [ ] Note down External Database URL (for backups)

### 2. Create Web Service
- [ ] Go to Render Dashboard → New → Web Service
- [ ] Connect your Git repository
- [ ] Name: `rdfs` (or your preferred name)
- [ ] Region: Same as database
- [ ] Branch: `main` (or your deployment branch)
- [ ] Runtime: Python 3
- [ ] Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- [ ] Start Command: `gunicorn rdfs.wsgi:application`
- [ ] Plan: Starter or higher

### 3. Configure Environment Variables

Go to your Web Service → Environment and add:

#### Core Settings
- [ ] `ENVIRONMENT` = `production`
- [ ] `SECRET_KEY` = `<generate-new-key>`
- [ ] `DEBUG` = `False`
- [ ] `PYTHON_VERSION` = `3.11.7`

#### Allowed Hosts
- [ ] `ALLOWED_HOSTS` = `your-app.onrender.com`

#### Database
- [ ] `DATABASE_URL` = `<Internal-Database-URL>`
  - Use Internal URL for better performance
  - Format: `postgresql://user:pass@host/db`

#### Cloudinary
- [ ] `CLOUDINARY_URL` = `cloudinary://key:secret@cloud`

#### Superuser
- [ ] `DJANGO_SUPERUSER_USERNAME` = `adminterminal`
- [ ] `DJANGO_SUPERUSER_EMAIL` = `admin@example.com`
- [ ] `DJANGO_SUPERUSER_PASSWORD` = `<strong-password>`

#### Session
- [ ] `SESSION_COOKIE_AGE` = `900`

#### Redis (Optional)
- [ ] `USE_REDIS_CHANNEL_LAYER` = `False`
- [ ] `REDIS_URL` = `redis://...` (if using Redis)

---

## Generate SECRET_KEY

**CRITICAL:** Generate a new SECRET_KEY for production!

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Copy the output and use it as your `SECRET_KEY` environment variable.

---

## Database Migration

Choose one option:

### Option A: Fresh Start (Recommended)
- [ ] Set `DATABASE_URL` to new Render PostgreSQL
- [ ] Deploy application
- [ ] Migrations run automatically
- [ ] Superuser created automatically
- [ ] Done!

### Option B: Migrate Existing Data
- [ ] Backup old database
- [ ] Verify backup successful
- [ ] Restore to new database
- [ ] Set `DATABASE_URL` to new Render PostgreSQL
- [ ] Deploy application
- [ ] Verify data migrated correctly

See `DATABASE_MIGRATION_CHECKLIST.md` for detailed steps.

---

## Deployment

### 1. Deploy Application
- [ ] Click "Manual Deploy" or push to connected branch
- [ ] Wait for build to complete
- [ ] Check build logs for errors
- [ ] Verify migrations ran successfully

### 2. Initial Verification
- [ ] Application deployed successfully
- [ ] No errors in deployment logs
- [ ] Service is "Live" in Render dashboard
- [ ] Can access application URL

---

## Post-Deployment Testing

### Basic Functionality
- [ ] Homepage loads
- [ ] Static files load (CSS, JS, images)
- [ ] No 404 errors for static files
- [ ] No console errors in browser

### Authentication
- [ ] Can access login page
- [ ] Can log in with superuser credentials
- [ ] Session persists correctly
- [ ] Can log out successfully

### Admin Dashboard
- [ ] Admin dashboard loads
- [ ] All metrics display correctly
- [ ] No database errors
- [ ] Charts render properly

### Staff Dashboard
- [ ] Staff dashboard loads
- [ ] All features accessible
- [ ] Forms work correctly

### Driver Management
- [ ] Can view drivers list
- [ ] Can add new driver
- [ ] Can edit driver
- [ ] Can upload driver photo
- [ ] Photos display correctly (Cloudinary)

### Vehicle Management
- [ ] Can view vehicles list
- [ ] Can add new vehicle
- [ ] Can edit vehicle
- [ ] QR codes generate correctly
- [ ] QR codes display correctly

### Terminal Operations
- [ ] QR scan entry works
- [ ] QR scan exit works
- [ ] Queue updates correctly
- [ ] Transactions recorded

### Reports
- [ ] Reports page loads
- [ ] Data displays correctly
- [ ] Charts render properly
- [ ] No calculation errors

### Media Uploads
- [ ] Can upload images
- [ ] Images stored in Cloudinary
- [ ] Images display correctly
- [ ] No upload errors

---

## Security Verification

### HTTPS
- [ ] Site loads with HTTPS
- [ ] No mixed content warnings
- [ ] SSL certificate valid

### Security Headers
- [ ] HSTS header present
- [ ] X-Frame-Options set
- [ ] Content-Type-Nosniff set
- [ ] XSS-Protection enabled

### Cookies
- [ ] Session cookies secure
- [ ] CSRF cookies secure
- [ ] Cookies work correctly

### Access Control
- [ ] Admin pages require admin role
- [ ] Staff pages require staff role
- [ ] Unauthorized access blocked
- [ ] Login required for protected pages

---

## Performance Check

### Response Times
- [ ] Homepage loads in < 2 seconds
- [ ] Dashboard loads in < 3 seconds
- [ ] Database queries optimized
- [ ] No N+1 query issues

### Database
- [ ] Using Internal Database URL
- [ ] Connection pooling working
- [ ] No connection errors
- [ ] Queries performing well

### Static Files
- [ ] Static files compressed (WhiteNoise)
- [ ] Static files cached
- [ ] No 404s for static files

---

## Monitoring Setup

### Render Dashboard
- [ ] Check metrics tab
- [ ] Set up alerts (optional)
- [ ] Monitor resource usage
- [ ] Review logs regularly

### Application Logs
- [ ] No error messages
- [ ] No warning messages
- [ ] Migrations logged correctly
- [ ] Requests logged properly

---

## Backup & Recovery

### Database Backup
- [ ] Test database backup command
- [ ] Store backup securely
- [ ] Document backup procedure
- [ ] Schedule regular backups

### Rollback Plan
- [ ] Document rollback steps
- [ ] Test rollback procedure
- [ ] Keep previous deployment available
- [ ] Have backup ready

---

## Documentation

### Update Documentation
- [ ] Update README with production URL
- [ ] Document any custom configurations
- [ ] Update team documentation
- [ ] Share credentials securely

### Team Communication
- [ ] Notify team of deployment
- [ ] Share production URL
- [ ] Provide login credentials
- [ ] Document any issues

---

## Final Checks

### Functionality
- [ ] All features working
- [ ] No broken links
- [ ] Forms submit correctly
- [ ] Data persists correctly

### User Experience
- [ ] UI renders correctly
- [ ] Responsive on mobile
- [ ] No layout issues
- [ ] Images load properly

### Data Integrity
- [ ] Database data correct
- [ ] Relationships intact
- [ ] No data loss
- [ ] Migrations complete

### Security
- [ ] DEBUG=False verified
- [ ] SECRET_KEY unique
- [ ] Credentials secure
- [ ] HTTPS working

---

## Post-Deployment

### Immediate (First Hour)
- [ ] Monitor logs for errors
- [ ] Test critical features
- [ ] Verify database connections
- [ ] Check resource usage

### First Day
- [ ] Monitor application performance
- [ ] Check for any errors
- [ ] Verify all features working
- [ ] Collect user feedback

### First Week
- [ ] Review logs daily
- [ ] Monitor database size
- [ ] Check resource usage
- [ ] Address any issues

### Ongoing
- [ ] Regular backups
- [ ] Monitor performance
- [ ] Update dependencies
- [ ] Security updates

---

## Troubleshooting

### If Deployment Fails
1. Check build logs for errors
2. Verify environment variables
3. Check database connection
4. Review settings.py
5. Test locally first

### If Application Errors
1. Check application logs
2. Verify DATABASE_URL
3. Check ALLOWED_HOSTS
4. Verify static files
5. Test database connection

### If Database Issues
1. Verify DATABASE_URL correct
2. Check database is running
3. Test connection manually
4. Review migration logs
5. Check database credentials

---

## Success Criteria

Deployment is successful when:

- ✅ Application accessible via HTTPS
- ✅ All features working correctly
- ✅ No errors in logs
- ✅ Database connected and working
- ✅ Static files loading
- ✅ Media uploads working
- ✅ Authentication working
- ✅ Security headers present
- ✅ Performance acceptable
- ✅ Team can access and use

---

## Support Resources

- **Render Docs:** https://render.com/docs
- **Django Docs:** https://docs.djangoproject.com/
- **Project Docs:** See documentation folder
- **Logs:** Render Dashboard → Logs

---

## Notes

- Keep this checklist for future deployments
- Update based on your experience
- Share with team members
- Document any custom steps

---

**Deployment Date:** _____________

**Deployed By:** _____________

**Production URL:** _____________

**Notes:** _____________
