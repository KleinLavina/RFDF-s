# Database Migration Checklist

## Switching from Neon to Render PostgreSQL

This checklist guides you through migrating from your current Neon database to the new Render PostgreSQL database.

---

## Pre-Migration

### 1. Backup Current Database (Neon)

```bash
# Export current database
pg_dump "postgresql://neondb_owner:npg_pXJ9lYwk2EoL@ep-muddy-water-ahpqjyj0-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require" > backup_$(date +%Y%m%d_%H%M%S).sql
```

### 2. Verify Backup

```bash
# Check backup file size
ls -lh backup_*.sql

# Verify backup content (first 50 lines)
head -n 50 backup_*.sql
```

### 3. Document Current State

- [ ] Note number of users
- [ ] Note number of drivers
- [ ] Note number of vehicles
- [ ] Note number of transactions
- [ ] Take screenshots of important data

---

## Migration Options

### Option A: Fresh Start (Recommended for Development)

**Best for:** Development, testing, or if you don't need to preserve data

**Steps:**

1. **Update DATABASE_URL in Render:**
   ```
   DATABASE_URL=postgresql://rdfs_database_user:5f4yOSRpmltsamQvKYLbWwfuJbroy90A@dpg-d5q3366r433s73fovhb0-a/rdfs_database
   ```

2. **Redeploy application** - Migrations will run automatically

3. **Verify deployment:**
   - Check logs for migration success
   - Access application
   - Log in with superuser credentials

4. **Done!** Fresh database is ready

---

### Option B: Migrate Existing Data

**Best for:** Production, or when you need to preserve existing data

#### Step 1: Prepare New Database

1. **Verify new database is empty:**
   ```bash
   psql "postgresql://rdfs_database_user:5f4yOSRpmltsamQvKYLbWwfuJbroy90A@dpg-d5q3366r433s73fovhb0-pooler.oregon-postgres.render.com/rdfs_database" -c "\dt"
   ```

2. **If not empty, clear it:**
   ```bash
   psql "postgresql://rdfs_database_user:5f4yOSRpmltsamQvKYLbWwfuJbroy90A@dpg-d5q3366r433s73fovhb0-pooler.oregon-postgres.render.com/rdfs_database" -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
   ```

#### Step 2: Restore Backup to New Database

```bash
# Restore backup to new database
psql "postgresql://rdfs_database_user:5f4yOSRpmltsamQvKYLbWwfuJbroy90A@dpg-d5q3366r433s73fovhb0-pooler.oregon-postgres.render.com/rdfs_database" < backup_YYYYMMDD_HHMMSS.sql
```

#### Step 3: Verify Data Migration

```bash
# Connect to new database
psql "postgresql://rdfs_database_user:5f4yOSRpmltsamQvKYLbWwfuJbroy90A@dpg-d5q3366r433s73fovhb0-pooler.oregon-postgres.render.com/rdfs_database"

# Check tables
\dt

# Check user count
SELECT COUNT(*) FROM accounts_customuser;

# Check driver count
SELECT COUNT(*) FROM vehicles_driver;

# Check vehicle count
SELECT COUNT(*) FROM vehicles_vehicle;

# Exit
\q
```

#### Step 4: Update Render Environment

1. **Go to Render Dashboard** → Your Web Service → Environment

2. **Update DATABASE_URL:**
   ```
   DATABASE_URL=postgresql://rdfs_database_user:5f4yOSRpmltsamQvKYLbWwfuJbroy90A@dpg-d5q3366r433s73fovhb0-a/rdfs_database
   ```
   
   **Important:** Use the **Internal Database URL** (without `-pooler`) for better performance

3. **Save changes** - This will trigger a redeploy

#### Step 5: Post-Migration Verification

1. **Check deployment logs:**
   - Look for successful migration messages
   - Check for any errors

2. **Test application:**
   - [ ] Can access homepage
   - [ ] Can log in
   - [ ] Can view drivers list
   - [ ] Can view vehicles list
   - [ ] Can create new entries
   - [ ] Can upload images
   - [ ] All features work as expected

3. **Verify data integrity:**
   - [ ] User accounts present
   - [ ] Drivers data intact
   - [ ] Vehicles data intact
   - [ ] Transactions preserved
   - [ ] Media files accessible

---

## Post-Migration

### 1. Monitor Application

- [ ] Check logs for errors
- [ ] Monitor database connections
- [ ] Watch for performance issues
- [ ] Test all critical features

### 2. Update Documentation

- [ ] Update team documentation with new database URL
- [ ] Update any scripts that reference old database
- [ ] Update backup procedures

### 3. Clean Up

- [ ] Keep backup file safe for at least 30 days
- [ ] Remove old database credentials from Render (after confirming everything works)
- [ ] Update any external tools/scripts

---

## Rollback Plan

If something goes wrong:

### Immediate Rollback

1. **Revert DATABASE_URL in Render:**
   ```
   DATABASE_URL=postgresql://neondb_owner:npg_pXJ9lYwk2EoL@ep-muddy-water-ahpqjyj0-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require
   ```

2. **Redeploy** - Application will reconnect to old database

3. **Verify** - Check that application works with old database

### If Data Was Lost

1. **Restore from backup:**
   ```bash
   psql "postgresql://rdfs_database_user:5f4yOSRpmltsamQvKYLbWwfuJbroy90A@dpg-d5q3366r433s73fovhb0-pooler.oregon-postgres.render.com/rdfs_database" < backup_YYYYMMDD_HHMMSS.sql
   ```

2. **Update DATABASE_URL** to new database

3. **Redeploy**

---

## Database URLs Reference

### Old Database (Neon)
```
External: postgresql://neondb_owner:npg_pXJ9lYwk2EoL@ep-muddy-water-ahpqjyj0-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require
```

### New Database (Render)
```
Internal (Use this): postgresql://rdfs_database_user:5f4yOSRpmltsamQvKYLbWwfuJbroy90A@dpg-d5q3366r433s73fovhb0-a/rdfs_database

External (For backups): postgresql://rdfs_database_user:5f4yOSRpmltsamQvKYLbWwfuJbroy90A@dpg-d5q3366r433s73fovhb0-pooler.oregon-postgres.render.com/rdfs_database
```

**Important:** Always use the **Internal URL** in your Render Web Service for better performance and lower latency.

---

## Troubleshooting

### Connection Refused
- Check database URL is correct
- Verify database is running in Render dashboard
- Ensure no typos in credentials

### Migration Errors
- Check Django migrations are up to date
- Run `python manage.py migrate` manually in Render shell
- Check logs for specific error messages

### Data Missing After Migration
- Verify backup was complete
- Check restore command completed successfully
- Restore from backup again if needed

### Performance Issues
- Ensure using Internal Database URL (not External)
- Check database plan/resources in Render
- Monitor database metrics in Render dashboard

---

## Support Commands

### Check Database Connection
```bash
python manage.py dbshell
```

### Run Migrations
```bash
python manage.py migrate
```

### Create Superuser
```bash
python manage.py create_admin
```

### Check Migration Status
```bash
python manage.py showmigrations
```

### Database Shell
```bash
python manage.py dbshell
```

---

## Timeline Estimate

- **Option A (Fresh Start):** 5-10 minutes
- **Option B (Data Migration):** 30-60 minutes (depending on data size)

---

## Success Criteria

- [ ] Application deploys successfully
- [ ] No errors in logs
- [ ] Can log in with credentials
- [ ] All data accessible (if migrated)
- [ ] All features working
- [ ] Performance is acceptable
- [ ] Backup stored safely
