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

/*
UPDATE works SET contract_id = (
    CASE WHEN EXISTS(
        SELECT associations_contract_project.contract_id
        FROM associations_contract_project
        WHERE associations_contract_project.id = works.association_contract_project_id
    ) THEN (
        SELECT associations_contract_project.contract_id
        FROM associations_contract_project
        WHERE associations_contract_project.id = works.association_contract_project_id
    ) ELSE (
        works.contract_id
    ) END
);

UPDATE works SET project_id = (
    CASE WHEN EXISTS(
        SELECT associations_contract_project.project_id
        FROM associations_contract_project
        WHERE associations_contract_project.id = works.association_contract_project_id
    ) THEN (
        SELECT associations_contract_project.project_id
        FROM associations_contract_project
        WHERE associations_contract_project.id = works.association_contract_project_id
    ) ELSE (
        works.project_id
    ) END
);
*/

DO $$ BEGIN
    IF EXISTS(
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = 'public'
            AND table_name = 'works'
            AND column_name = 'association_contract_project_id'
    ) THEN
        UPDATE works SET contract_id = (
            SELECT associations_contract_project.contract_id
            FROM associations_contract_project
            WHERE associations_contract_project.id = works.association_contract_project_id
        );
        UPDATE works SET project_id = (
            SELECT associations_contract_project.project_id
            FROM associations_contract_project
            WHERE associations_contract_project.id = works.association_contract_project_id
        );
    END IF ;
END $$ ;

ALTER TABLE IF EXISTS works
    DROP CONSTRAINT IF EXISTS work_association_contract_project_fk,
    DROP COLUMN IF EXISTS association_contract_project_id;
