ALTER TABLE IF EXISTS works
    DROP CONSTRAINT IF EXISTS work_association_contract_project_fk,
    DROP COLUMN IF EXISTS association_contract_project_id;
