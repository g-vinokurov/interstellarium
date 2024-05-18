ALTER TABLE IF EXISTS users
    DROP CONSTRAINT IF EXISTS user_department_department_fk,
    DROP COLUMN IF EXISTS department_id;
