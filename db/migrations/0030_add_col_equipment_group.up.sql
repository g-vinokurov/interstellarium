ALTER TABLE IF EXISTS equipment
    ADD COLUMN IF NOT EXISTS group_id INTEGER NULL;

ALTER TABLE IF EXISTS equipment
    DROP CONSTRAINT IF EXISTS equipment_group_fk,
    ADD CONSTRAINT equipment_group_fk
        FOREIGN KEY (group_id)
        REFERENCES groups (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE;
