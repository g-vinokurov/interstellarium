CREATE TABLE IF NOT EXISTS technicians (
	id      SERIAL NOT NULL,
	user_id INTEGER NOT NULL,
	CONSTRAINT technician_pk PRIMARY KEY (id),
	CONSTRAINT technician_user_fk FOREIGN KEY(user_id)
	    REFERENCES users (id)
	    ON DELETE CASCADE
	    ON UPDATE CASCADE
);
