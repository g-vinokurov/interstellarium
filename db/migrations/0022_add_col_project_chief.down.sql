ALTER TABLE IF EXISTS projects
    DROP CONSTRAINT IF EXISTS project_chief_fk,
    DROP COLUMN IF EXISTS chief_id;
