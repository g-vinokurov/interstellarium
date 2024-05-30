ALTER TABLE IF EXISTS contracts
    ADD COLUMN IF NOT EXISTS group_id INTEGER NULL;

ALTER TABLE IF EXISTS contracts
    DROP CONSTRAINT IF EXISTS contract_group_fk,
    ADD CONSTRAINT contract_group_fk
        FOREIGN KEY (group_id)
        REFERENCES groups (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE;
