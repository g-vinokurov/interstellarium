ALTER TABLE IF EXISTS assignments_user_project
    ADD COLUMN IF NOT EXISTS assignment_date DATE NULL,
    ADD COLUMN IF NOT EXISTS is_assigned BOOLEAN NULL;
