# Yoyo SQL Migrations Guide
Guide for managing database migrations using Yoyo-migrations with SQL files.

## Configuration
Your project should have a yoyo.ini file:

```
[DEFAULT]
sources = ./migrations
database = postgresql://user:password@localhost/dbname
migration_table = _yoyo_migration
batch_mode = on
```

## Creating Migrations
### Create a new migration

```Bash
yoyo new -m "description_of_your_migration" --sql
```

This creates a new .sql file in your migrations folder:

```PostgreSQL
-- description_of_your_migration
-- depends: previous_migration_id

-- Write your SQL migration here

CREATE TABLE example (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);
```

For create a rollback script copy name of apply script and add .rollback before .sql.

```PostgreSQL
-- Write your SQL rollback migration here
DROP TABLE example;
```

### Running Migrations

```
# Apply pending migrations
yoyo apply

# Rollback last migration
yoyo rollback

# Show migration status
yoyo list

Common Commands
# Check migration status
yoyo status

# Apply with verbosity
yoyo apply --verbose

# Rollback specific number of migrations
yoyo rollback --count N
```

Best Practices
- Always include rollback steps
- Use descriptive migration names
- Test migrations in development
- Keep migrations atomic
- Back up database before applying migrations