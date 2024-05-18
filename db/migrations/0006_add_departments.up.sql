CREATE TABLE IF NOT EXISTS departments (
	id        SERIAL NOT NULL,
	leader_id INTEGER NOT NULL,
	CONSTRAINT department_pk PRIMARY KEY (id),
	CONSTRAINT department_leader_user_fk FOREIGN KEY(leader_id)
	    REFERENCES users (id)
	    ON DELETE CASCADE
	    ON UPDATE CASCADE
);
