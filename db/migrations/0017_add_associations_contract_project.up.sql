CREATE TABLE IF NOT EXISTS associations_contract_project (
    id SERIAL NOT NULL,
    contract_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    CONSTRAINT association_contract_project_pk PRIMARY KEY (id),
    CONSTRAINT association_contract_project_contract_fk FOREIGN KEY(contract_id)
        REFERENCES contracts (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT association_contract_project_project_fk FOREIGN KEY(project_id)
        REFERENCES projects (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
