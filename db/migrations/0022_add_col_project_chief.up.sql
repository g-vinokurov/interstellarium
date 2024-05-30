ALTER TABLE IF EXISTS projects
    ADD COLUMN IF NOT EXISTS chief_id INTEGER NULL;

ALTER TABLE IF EXISTS projects
    DROP CONSTRAINT IF EXISTS project_chief_fk,
    ADD CONSTRAINT project_chief_fk
        FOREIGN KEY (chief_id)
        REFERENCES users (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE;
