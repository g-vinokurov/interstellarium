ALTER TABLE IF EXISTS assignments_user_project
    DROP COLUMN IF EXISTS assignment_date,
    DROP COLUMN IF EXISTS is_assigned;
