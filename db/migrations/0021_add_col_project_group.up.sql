ALTER TABLE IF EXISTS projects
    ADD COLUMN IF NOT EXISTS group_id INTEGER NULL;

ALTER TABLE IF EXISTS projects
    DROP CONSTRAINT IF EXISTS project_group_fk,
    ADD CONSTRAINT project_group_fk
        FOREIGN KEY (group_id)
        REFERENCES groups (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE;
