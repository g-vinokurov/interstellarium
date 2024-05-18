CREATE TABLE IF NOT EXISTS designers (
	id INTEGER AUTOINCREMENT NOT NULL,
	user_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
);
