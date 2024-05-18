CREATE TABLE IF NOT EXISTS designers (
	id      SERIAL NOT NULL,
	user_id INTEGER NOT NULL, 
	CONSTRAINT designer_pk PRIMARY KEY (id), 
	CONSTRAINT designer_user_fk FOREIGN KEY(user_id)
	    REFERENCES users (id)
	    ON DELETE CASCADE
	    ON UPDATE CASCADE
);
