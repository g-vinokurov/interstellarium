ALTER TABLE IF EXISTS contracts
    DROP CONSTRAINT IF EXISTS contract_group_fk,
    DROP COLUMN IF EXISTS group_id;
