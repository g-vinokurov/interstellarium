ALTER TABLE IF EXISTS users
    ADD COLUMN IF NOT EXISTS department_id INTEGER NULL,
    DROP CONSTRAINT IF EXISTS user_department_department_fk,
    ADD CONSTRAINT user_department_department_fk FOREIGN KEY(department_id)
	    REFERENCES departments (id)
	    ON DELETE SET NULL
	    ON UPDATE CASCADE;
