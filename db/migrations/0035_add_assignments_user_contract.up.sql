CREATE TABLE IF NOT EXISTS assignments_user_contract (
    id SERIAL NOT NULL,
    user_id INTEGER NOT NULL,
    contract_id INTEGER NOT NULL,
    assignment_date DATE NULL,
    is_assigned BOOLEAN NULL,
    CONSTRAINT assignment_user_contract_pk PRIMARY KEY (id),
    CONSTRAINT assignment_user_contract_user_fk FOREIGN KEY(user_id)
        REFERENCES users (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT assignment_user_contract_contract_fk FOREIGN KEY(contract_id)
        REFERENCES contracts (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
