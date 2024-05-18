CREATE TABLE IF NOT EXISTS engineers (
	id      SERIAL NOT NULL,
	user_id INTEGER NOT NULL, 
	CONSTRAINT engineer_pk PRIMARY KEY (id), 
	CONSTRAINT engineer_user_fk FOREIGN KEY(user_id)
	    REFERENCES users (id)
	    ON DELETE CASCADE
	    ON UPDATE CASCADE
);
