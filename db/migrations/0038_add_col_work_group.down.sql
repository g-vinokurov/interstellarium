ALTER TABLE IF EXISTS works
    DROP CONSTRAINT IF EXISTS work_group_fk,
    DROP COLUMN IF EXISTS group_id;