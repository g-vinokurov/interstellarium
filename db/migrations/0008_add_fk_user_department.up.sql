ALTER TABLE IF EXISTS users
    ADD COLUMN department_id INTEGER NULL,
    ADD CONSTRAINT user_department_department_fk FOREIGN KEY(department_id)
	    REFERENCES departments (id)
	    ON DELETE SET NULL
	    ON UPDATE CASCADE;
