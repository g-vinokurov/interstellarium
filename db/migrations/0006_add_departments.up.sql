CREATE TABLE IF NOT EXISTS departments (
	id        SERIAL NOT NULL,
	chief_id INTEGER NOT NULL,
	CONSTRAINT department_pk PRIMARY KEY (id),
	CONSTRAINT department_chief_user_fk FOREIGN KEY(chief_id)
	    REFERENCES users (id)
	    ON DELETE CASCADE
	    ON UPDATE CASCADE
);
