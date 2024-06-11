CREATE TABLE IF NOT EXISTS associations_user_group (
    id SERIAL NOT NULL,
    user_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    CONSTRAINT association_user_group_pk PRIMARY KEY (id),
    CONSTRAINT association_user_group_user_fk FOREIGN KEY(user_id)
        REFERENCES users (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT association_user_group_group_fk FOREIGN KEY(group_id)
        REFERENCES groups (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
