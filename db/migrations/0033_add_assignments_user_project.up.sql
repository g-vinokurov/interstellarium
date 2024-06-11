CREATE TABLE IF NOT EXISTS assignments_user_project (
    id SERIAL NOT NULL,
    user_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    CONSTRAINT assignment_user_project_pk PRIMARY KEY (id),
    CONSTRAINT assignment_user_project_user_fk FOREIGN KEY(user_id)
        REFERENCES users (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT assignment_user_project_project_fk FOREIGN KEY(project_id)
        REFERENCES projects (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
