ALTER TABLE IF EXISTS works
    ADD COLUMN IF NOT EXISTS contract_id INTEGER NULL;

ALTER TABLE IF EXISTS works
    ADD COLUMN IF NOT EXISTS project_id INTEGER NULL;

ALTER TABLE IF EXISTS works
    DROP CONSTRAINT IF EXISTS work_contract_fk,
    ADD CONSTRAINT work_contract_fk
        FOREIGN KEY (contract_id)
        REFERENCES contracts (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE;

ALTER TABLE IF EXISTS works
    DROP CONSTRAINT IF EXISTS work_project_fk,
    ADD CONSTRAINT work_project_fk
        FOREIGN KEY (project_id)
        REFERENCES projects (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE;
