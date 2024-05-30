ALTER TABLE IF EXISTS contracts
    ADD COLUMN IF NOT EXISTS chief_id INTEGER NULL;

ALTER TABLE IF EXISTS contracts
    DROP CONSTRAINT IF EXISTS contract_chief_fk,
    ADD CONSTRAINT contract_chief_fk
        FOREIGN KEY (chief_id)
        REFERENCES users (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE;
