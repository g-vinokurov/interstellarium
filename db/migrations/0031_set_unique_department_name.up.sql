ALTER TABLE IF EXISTS departments
    DROP CONSTRAINT IF EXISTS department_name_unique,
    ADD CONSTRAINT department_name_unique UNIQUE (name);
