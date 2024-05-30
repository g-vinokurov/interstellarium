ALTER TABLE IF EXISTS works
    ADD COLUMN IF NOT EXISTS association_contract_project_id INTEGER NULL;

ALTER TABLE IF EXISTS works
    DROP CONSTRAINT IF EXISTS work_association_contract_project_fk,
    ADD CONSTRAINT work_association_contract_project_fk
        FOREIGN KEY (association_contract_project_id)
        REFERENCES associations_contract_project (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE;
