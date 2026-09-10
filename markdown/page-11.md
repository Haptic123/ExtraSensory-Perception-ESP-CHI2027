# Database Backup and Restore

# Purpose

This page explains how to create a database dump and restore or update a local database from a SQL file.

# Create a dump file

Use `pg_dump` to export a database into a SQL file.

```bash
pg_dump -h hostname -U username -d databasename -f path/to/your_dump.sql
```

Example:

```bash
pg_dump -h localhost -U postgres -d smartwatchsys_db -f ./smartwatchsys_db_dump.sql
```

### Or

1. Open *PgAdmin*
2. Right click the `smartwatchsys_db` database
3. Choose “backup”
4. Enter filename (e.g., NEW_DB.sql), make sure it ends with .sql
5. For format choose “Plain”
6. Click the Backup button. The file is usually save in the “Documents” folder on your computer

[REMOVED FOR ANONYMITY]

# Update a local database


💡 After each step you’ll need to type your Postgres password, make sure you have it



1. Open the folder with the SQL backup file in CMD
2. Force disconnect anyone or any tool using the database right now
    
    ```bash
    psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'smartwatchsys_db' AND pid <> pg_backend_pid();"
    ```
    
3. Drop the current database instance
    
    ```bash
    dropdb -U postgres -h localhost smartwatchsys_db
    ```
    
4. Create a new database with the exact same name `smartwatchsys_db`
    
    ```bash
    createdb -U postgres smartwatchsys_db
    ```
    
5. Upload the SQL backup file to the database
    
    ```bash
    psql -U postgres -d smartwatchsys_db -f XXXXX.sql
    ```
    

# Restore a local database

Use this command pattern:

```bash
psql -h hostname -U username -d databasename -f path/to/your_file.sql
```

Example:

```bash
psql -h localhost -U postgres -d smartwatchsys_db -f ./DB_WITH_LOGGING.sql
```

# If the database does not exist yet

Create it first:

```sql
CREATE DATABASE smartwatchsys_db;
```

Then run the restore command.

# Verify after restoring

```sql
SELECT COUNT(*) FROM "UseCase";
SELECT COUNT(*) FROM feedback_config_rules WHERE active = true;
SELECT COUNT(*) FROM "User";
SELECT * FROM user_schedules LIMIT 10;
```