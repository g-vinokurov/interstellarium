ALTER TABLE IF EXISTS works
    ADD COLUMN IF NOT EXISTS association_contract_project_id INTEGER NULL;

ALTER TABLE IF EXISTS works
    DROP CONSTRAINT IF EXISTS work_association_contract_project_fk,
    ADD CONSTRAINT work_association_contract_project_fk
        FOREIGN KEY (association_contract_project_id)
        REFERENCES associations_contract_project (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE;

DO $$ BEGIN
    IF EXISTS(
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = 'public'
            AND table_name = 'works'
            AND column_name = 'contract_id'
    ) THEN
        UPDATE works SET association_contract_project_id = (
            SELECT associations_contract_project.id
            FROM associations_contract_project
            WHERE associations_contract_project.contract_id = works.contract_id
                AND associations_contract_project.project_id = works.project_id
        );
        UPDATE works SET project_id = (
            SELECT associations_contract_project.project_id
            FROM associations_contract_project
            WHERE associations_contract_project.id = works.association_contract_project_id
        );

        ALTER TABLE IF EXISTS works
            DROP CONSTRAINT IF EXISTS work_contract_fk;
        ALTER TABLE IF EXISTS works
            DROP CONSTRAINT IF EXISTS work_project_fk;
        ALTER TABLE IF EXISTS works
            DROP COLUMN IF EXISTS contract_id;
        ALTER TABLE IF EXISTS works
            DROP COLUMN IF EXISTS project_id;
    END IF ;
END $$ ;
