ALTER TABLE IF EXISTS equipment
    DROP CONSTRAINT IF EXISTS equipment_group_fk,
    DROP COLUMN IF EXISTS group_id;
