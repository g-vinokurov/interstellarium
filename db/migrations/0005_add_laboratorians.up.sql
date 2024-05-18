CREATE TABLE IF NOT EXISTS laboratorians (
	id      SERIAL NOT NULL,
	user_id INTEGER NOT NULL, 
	CONSTRAINT laboratorian_pk PRIMARY KEY (id), 
	CONSTRAINT laboratorian_user_fk FOREIGN KEY(user_id)
	    REFERENCES users (id)
	    ON DELETE CASCADE
	    ON UPDATE CASCADE
);
