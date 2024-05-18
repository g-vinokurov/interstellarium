CREATE TABLE IF NOT EXISTS users (
	id            SERIAL NOT NULL,
	email         VARCHAR(255) NOT NULL,
	password_hash VARCHAR(512) NOT NULL, 
	is_superuser  BOOLEAN NOT NULL,
	name          VARCHAR(255),
	CONSTRAINT user_pk PRIMARY KEY (id), 
	CONSTRAINT user_email_unique UNIQUE (email)
);
