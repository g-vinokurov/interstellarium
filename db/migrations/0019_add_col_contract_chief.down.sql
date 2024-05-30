ALTER TABLE IF EXISTS contracts
    DROP CONSTRAINT IF EXISTS contract_chief_fk,
    DROP COLUMN IF EXISTS chief_id;
